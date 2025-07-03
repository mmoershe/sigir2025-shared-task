from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

import os

CURRENT_DIRECTORY: str = os.path.dirname(__file__)
lora_adapter_dir: str = os.path.join(CURRENT_DIRECTORY, "block_checkpoint")

# Path or repo ID of your base model
base_model_path = "meta-llama/Llama-3.2-3B"

# Load tokenizer (from LoRA dir or base model)
tokenizer = AutoTokenizer.from_pretrained(lora_adapter_dir)

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(base_model_path)

# Load LoRA adapters onto the base model
model = PeftModel.from_pretrained(base_model, lora_adapter_dir).to("cuda")

# Prompt the model
prompt = "climate change fires danger prediction Output:"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=100)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))