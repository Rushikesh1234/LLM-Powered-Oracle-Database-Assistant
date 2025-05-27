import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Base model (must match training setup)
base_model_name = "meta-llama/Llama-3.2-1B-Instruct"
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    torch_dtype=torch.float32, 
)

# Load LoRA adapter
model = PeftModel.from_pretrained(base_model, "./trained_model")

# Merge LoRA adapter weights into base model
model = model.merge_and_unload()

# Save merged model
model.save_pretrained("./merged_model")
tokenizer = AutoTokenizer.from_pretrained(base_model_name)
tokenizer.save_pretrained("./merged_model")

print("✅ Merged model saved to ./merged_model")
