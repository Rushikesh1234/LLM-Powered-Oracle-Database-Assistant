import os
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from peft import get_peft_model, LoraConfig, TaskType

# Load Hugging Face token from environment variable
hf_token = os.getenv("HUGGINGFACE_TOKEN")
if not hf_token:
    raise ValueError("Please set HUGGINGFACE_TOKEN in your environment.")

# Load tokenizer
model_name = "meta-llama/Llama-3.2-1B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
tokenizer.pad_token = tokenizer.eos_token  

# Load model safely on MPS
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float32,  
    token=hf_token
).to("mps") 

# PEFT LoRA configuration (lightweight fine-tuning)
peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    inference_mode=False,
    r=8,
    lora_alpha=16,
    lora_dropout=0.1,
)
model = get_peft_model(model, peft_config)

# Load dataset
dataset = load_dataset("json", data_files="oracle_training_dataset.jsonl")["train"]

# Format chat-like data into plain text format
def format_conversation(example):
    messages = example["messages"]
    text = ""
    for msg in messages:
        text += f"<|{msg['role']}|>: {msg['content']}\n"
    return {
        "input_ids": tokenizer(
            text,
            padding="max_length",
            truncation=True,
            max_length=256  # Reduced to save memory on MPS
        )["input_ids"]
    }

dataset = dataset.map(format_conversation, remove_columns=["messages"])

# Data collator
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)

# Training arguments (optimized for Mac MPS)
training_args = TrainingArguments(
    output_dir="./outputs",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_train_epochs=2,
    logging_steps=10,
    save_strategy="epoch",
    save_total_limit=2,
    learning_rate=2e-4,
    warmup_steps=5,
    bf16=False,
    fp16=False, 
    push_to_hub=False,
    report_to="none"
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

# Train model
trainer.train()

# Save final model
model.save_pretrained("./trained_model")
tokenizer.save_pretrained("./trained_model")