import os
import pandas as pd
import torch
from transformers import (
    PegasusForConditionalGeneration, PegasusTokenizer,
    BertForSequenceClassification, BertTokenizer,
    AutoModelForSequenceClassification, AutoTokenizer,
    Trainer, TrainingArguments
)
from datasets import Dataset
from config import CNN_DAILYMAIL_PATH, BILLSUM_PATH, MODEL_DIR, PEGASUS_MODEL_NAME, BERT_MODEL_NAME, LEGALBERT_MODEL_NAME

def load_or_finetune_pegasus():
    model_path = os.path.join(MODEL_DIR, "pegasus")
    if os.path.exists(model_path):
        print("Loading fine-tuned Pegasus model...")
        tokenizer = PegasusTokenizer.from_pretrained(model_path)
        model = PegasusForConditionalGeneration.from_pretrained(model_path)
    else:
        print("Fine-tuning Pegasus model...")
        tokenizer = PegasusTokenizer.from_pretrained(PEGASUS_MODEL_NAME)
        model = PegasusForConditionalGeneration.from_pretrained(PEGASUS_MODEL_NAME)
        
        df = pd.read_csv(CNN_DAILYMAIL_PATH)
        if "article" not in df.columns or "highlights" not in df.columns:
            raise KeyError(f"CNN/DailyMail CSV must have 'article' and 'highlights' columns. Found: {list(df.columns)}")
        df = df[["article", "highlights"]].sample(n=1000, random_state=42)
        dataset = Dataset.from_pandas(df.rename(columns={"article": "document", "highlights": "summary"}))
        
        def preprocess_function(examples):
            inputs = tokenizer(examples["document"], max_length=512, truncation=True, padding="max_length")
            targets = tokenizer(examples["summary"], max_length=150, truncation=True, padding="max_length")
            inputs["labels"] = targets["input_ids"]
            return inputs
        
        tokenized_dataset = dataset.map(preprocess_function, batched=True)
        train_dataset = tokenized_dataset.select(range(800))
        eval_dataset = tokenized_dataset.select(range(800, 1000))
        
        training_args = TrainingArguments(
            output_dir="./pegasus_finetune",
            num_train_epochs=1,
            per_device_train_batch_size=1,
            per_device_eval_batch_size=1,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir="./logs",
            logging_steps=10,
            eval_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
        )
        
        trainer = Trainer(model=model, args=training_args, train_dataset=train_dataset, eval_dataset=eval_dataset)
        trainer.train()
        trainer.save_model(model_path)
        tokenizer.save_pretrained(model_path)
        print(f"Fine-tuned Pegasus model saved to {model_path}")
    
    return tokenizer, model

def load_or_finetune_bert():
    model_path = os.path.join(MODEL_DIR, "bert")
    if os.path.exists(model_path):
        print("Loading fine-tuned BERT model...")
        tokenizer = BertTokenizer.from_pretrained(model_path)
        model = BertForSequenceClassification.from_pretrained(model_path)
    else:
        print("Fine-tuning BERT model...")
        tokenizer = BertTokenizer.from_pretrained(BERT_MODEL_NAME)
        model = BertForSequenceClassification.from_pretrained(BERT_MODEL_NAME, num_labels=2)
        
        df = pd.read_csv(CNN_DAILYMAIL_PATH)
        if "article" not in df.columns:
            raise KeyError(f"CNN/DailyMail CSV must have 'article' column. Found: {list(df.columns)}")
        df = df[["article"]].sample(n=400, random_state=42)
        dataset = Dataset.from_pandas(df)
        
        def preprocess_function(examples):
            inputs = tokenizer(examples["article"], max_length=512, truncation=True, padding="max_length")
            inputs["labels"] = torch.tensor([1 if len(t.split()) > 50 else 0 for t in examples["article"]])
            return inputs
        
        tokenized_dataset = dataset.map(preprocess_function, batched=True)
        train_dataset = tokenized_dataset.select(range(320))
        eval_dataset = tokenized_dataset.select(range(320, 400))
        
        training_args = TrainingArguments(
            output_dir="./bert_finetune",
            num_train_epochs=1,
            per_device_train_batch_size=1,
            per_device_eval_batch_size=1,
            warmup_steps=100,
            weight_decay=0.01,
            logging_dir="./logs",
            logging_steps=10,
            eval_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
        )
        
        trainer = Trainer(model=model, args=training_args, train_dataset=train_dataset, eval_dataset=eval_dataset)
        trainer.train()
        trainer.save_model(model_path)
        tokenizer.save_pretrained(model_path)
        print(f"Fine-tuned BERT model saved to {model_path}")
    
    return tokenizer, model

def load_or_finetune_legalbert():
    model_path = os.path.join(MODEL_DIR, "legalbert")
    if os.path.exists(model_path):
        print("Loading fine-tuned LegalBERT model...")
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
    else:
        print("Fine-tuning LegalBERT model...")
        tokenizer = AutoTokenizer.from_pretrained(LEGALBERT_MODEL_NAME)
        model = AutoModelForSequenceClassification.from_pretrained(LEGALBERT_MODEL_NAME, num_labels=2)
        
        df = pd.read_json(BILLSUM_PATH, lines=True)
        if "text" not in df.columns:
            raise KeyError(f"BillSum JSONL must have 'text' column. Found: {list(df.columns)}")
        df = df[["text"]].sample(n=400, random_state=42)
        dataset = Dataset.from_pandas(df)
        
        def preprocess_function(examples):
            inputs = tokenizer(examples["text"], max_length=512, truncation=True, padding="max_length")
            inputs["labels"] = torch.tensor([1 if any(kw in t.lower() for kw in ["law", "court"]) else 0 for t in examples["text"]])
            return inputs
        
        tokenized_dataset = dataset.map(preprocess_function, batched=True)
        train_dataset = tokenized_dataset.select(range(320))
        eval_dataset = tokenized_dataset.select(range(320, 400))
        
        training_args = TrainingArguments(
            output_dir="./legalbert_finetune",
            num_train_epochs=1,
            per_device_train_batch_size=1,
            per_device_eval_batch_size=1,
            warmup_steps=100,
            weight_decay=0.01,
            logging_dir="./logs",
            logging_steps=10,
            eval_strategy="epoch",
            save_strategy="epoch",
            load_best_model_at_end=True,
        )
        
        trainer = Trainer(model=model, args=training_args, train_dataset=train_dataset, eval_dataset=eval_dataset)
        trainer.train()
        trainer.save_model(model_path)
        tokenizer.save_pretrained(model_path)
        print(f"Fine-tuned LegalBERT model saved to {model_path}")
    
    return tokenizer, model