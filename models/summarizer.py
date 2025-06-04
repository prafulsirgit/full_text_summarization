import torch
import numpy as np

def summarize_with_pegasus(text, tokenizer, model, length="normal"):
    inputs = tokenizer(text, truncation=True, padding="longest", return_tensors="pt", max_length=512)
    length_params = {"normal": (150, 30, 2.0), "long": (300, 60, 1.5)}
    max_length, min_length, length_penalty = length_params.get(length, (150, 30, 2.0))
    summary_ids = model.generate(inputs["input_ids"], max_length=max_length, min_length=min_length, length_penalty=length_penalty, num_beams=4)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def summarize_with_bert(text, tokenizer, model):
    sentences = text.split(". ")
    if len(sentences) < 2:
        return text
    inputs = tokenizer(sentences, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    scores = outputs.logits[:, 1].numpy()
    key_sentence_idx = scores.argsort()[-2:][::-1]
    return ". ".join([sentences[idx] for idx in key_sentence_idx if sentences[idx].strip()])

def summarize_with_legalbert(text, tokenizer, model):
    sentences = text.split(". ")
    if len(sentences) < 2:
        return text
    inputs = tokenizer(sentences, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    scores = outputs.logits[:, 1].numpy()
    key_sentence_idx = scores.argsort()[-2:][::-1]
    return ". ".join([sentences[idx] for idx in key_sentence_idx if sentences[idx].strip()])