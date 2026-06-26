import argparse
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer, DataCollatorWithPadding

MODEL_NAME = "skt/kobert-base-v1"
LABELS = ["기관사칭", "금전요구", "긴급압박", "가족사칭", "개인정보", "앱설치유도", "가입유도"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--output", default="models/kobert_multilabel")
    parser.add_argument("--epochs", type=int, default=3)
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    df["text"] = df["text"].astype(str)
    for label in LABELS:
        if label not in df.columns:
            df[label] = 0
        df[label] = df[label].astype(float)

    train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)

    def make_dataset(frame):
        rows = []
        for _, row in frame.iterrows():
            rows.append({"text": str(row["text"]), "labels": [float(row[label]) for label in LABELS]})
        ds = Dataset.from_list(rows)
        def tok(batch):
            tokenized = tokenizer(batch["text"], truncation=True, max_length=256, padding=False)
            tokenized["labels"] = batch["labels"]
            return tokenized
        return ds.map(tok, batched=True, remove_columns=["text"])

    train_ds = make_dataset(train_df)
    val_ds = make_dataset(val_df)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(LABELS),
        problem_type="multi_label_classification",
        id2label={i: label for i, label in enumerate(LABELS)},
        label2id={label: i for i, label in enumerate(LABELS)},
        trust_remote_code=True,
    )

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        probs = 1 / (1 + np.exp(-logits))
        preds = (probs >= 0.5).astype(int)
        return {"micro_f1": f1_score(labels, preds, average="micro", zero_division=0)}

    args_train = TrainingArguments(
        output_dir=args.output + "_checkpoints",
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=args.epochs,
        load_best_model_at_end=True,
        metric_for_best_model="micro_f1",
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=args_train,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        data_collator=DataCollatorWithPadding(tokenizer),
        compute_metrics=compute_metrics,
    )

    trainer.train()
    trainer.save_model(args.output)
    tokenizer.save_pretrained(args.output)
    print("저장 완료:", args.output)

if __name__ == "__main__":
    main()
