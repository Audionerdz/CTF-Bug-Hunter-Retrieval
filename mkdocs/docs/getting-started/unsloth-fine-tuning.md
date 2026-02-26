# Fine-Tuning with Unsloth (from Atlas Engine ChatML Logs)

Atlas Engine automatically logs every conversation in ChatML/ShareGPT format. This guide shows how to use those logs to fine-tune your own LLM with Unsloth.

## Pipeline Overview

```
Atlas Engine chat sessions
        |
        v
chat_history/session_*_chatml.jsonl   (auto-generated)
        |
        v
Unsloth fine-tuning (QLoRA, 4-bit)
        |
        v
Export to GGUF / Ollama / vLLM / HuggingFace
```

## Step 1: Generate Training Data

Use Atlas Engine normally. Every `.ask()` or `.chat()` call logs conversations automatically.

```bash
cd /home/kali/Desktop/RAG
source venv/bin/activate && python3
```

```python
from atlas_engine import Atlas
atlas = Atlas()
atlas.chat(backend="groq")    # or gpt, gemini, ollama
# have conversations, ask questions, build up data
# type 'exit' when done
```

Your logs are in:

```bash
ls chat_history/
# session_groq_20260226_160000_chatml.jsonl
# session_gpt_20260226_161500_chatml.jsonl
```

Each line is one training example in ShareGPT format:

```json
{
  "conversations": [
    {"from": "system", "value": "Identity: You are Atlas Engine..."},
    {"from": "human", "value": "Context:...\n\nQuestion: What is LFI?"},
    {"from": "gpt", "value": "LFI allows reading local files..."}
  ]
}
```

## Step 2: Merge Sessions (Optional)

If you have multiple session files and want to train on all of them:

```bash
cat chat_history/session_*_chatml.jsonl > chat_history/training_data.jsonl
```

Check how many examples you have:

```bash
wc -l chat_history/training_data.jsonl
```

Minimum recommended: 100+ examples for reasonable results.

## Step 3: Install Unsloth

### Requirements

- Linux or WSL (Windows)
- NVIDIA GPU with 6GB+ VRAM (8GB+ recommended)
- Python 3.10, 3.11, or 3.12 (3.13 now supported)
- CUDA drivers installed

### Install

Create a separate venv for Unsloth (do not mix with Atlas venv):

```bash
cd /home/kali/Desktop
python3 -m venv unsloth_env
source unsloth_env/bin/activate
pip install --upgrade pip
pip install unsloth
```

This installs torch, transformers, bitsandbytes, triton, trl, and all dependencies automatically.

Verify:

```bash
python3 -c "from unsloth import FastLanguageModel; print('Unsloth ready')"
```

## Step 4: Fine-Tune

Create a file called `train.py`:

```python
from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template, standardize_sharegpt
from datasets import load_dataset
from trl import SFTTrainer, SFTConfig

# =============================================
# 1. LOAD MODEL
# =============================================
# Change model_name to any model from HuggingFace.
# Recommended starters:
#   "unsloth/llama-3.1-8b-instruct-bnb-4bit"
#   "unsloth/mistral-7b-instruct-v0.3-bnb-4bit"
#   "unsloth/gemma-2-9b-it-bnb-4bit"
#   "unsloth/Qwen2.5-7B-Instruct-bnb-4bit"

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/llama-3.1-8b-instruct-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
)

# =============================================
# 2. ADD LORA ADAPTERS
# =============================================
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    lora_alpha=16,
    lora_dropout=0,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],
    use_gradient_checkpointing="unsloth",
)

# =============================================
# 3. LOAD YOUR ATLAS ENGINE DATA
# =============================================
# Point this to your ChatML JSONL file(s)
dataset = load_dataset(
    "json",
    data_files="/home/kali/Desktop/RAG/chat_history/training_data.jsonl",
    split="train",
)

# Convert ShareGPT format ("from"/"value") to standard format
dataset = standardize_sharegpt(dataset)

# Apply chat template
tokenizer = get_chat_template(
    tokenizer,
    chat_template="llama-3.1",
    mapping={
        "role": "from",
        "content": "value",
        "user": "human",
        "assistant": "gpt",
    },
)

def formatting_func(examples):
    convos = examples["conversations"]
    texts = [
        tokenizer.apply_chat_template(c, tokenize=False, add_generation_prompt=False)
        for c in convos
    ]
    return {"text": texts}

dataset = dataset.map(formatting_func, batched=True)

# =============================================
# 4. TRAIN
# =============================================
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    args=SFTConfig(
        dataset_text_field="text",
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        num_train_epochs=3,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=1,
        output_dir="outputs",
        seed=3407,
    ),
)

print(f"Training on {len(dataset)} examples...")
trainer.train()

# =============================================
# 5. SAVE
# =============================================

# Save LoRA adapter (small, ~100MB)
model.save_pretrained("atlas_lora")
tokenizer.save_pretrained("atlas_lora")
print("LoRA adapter saved to: atlas_lora/")

# Save merged 16-bit model (for vLLM deployment)
# model.save_pretrained_merged("atlas_merged", tokenizer, save_method="merged_16bit")

# Save as GGUF (for Ollama / llama.cpp)
# model.save_pretrained_gguf("atlas_gguf", tokenizer, quantization_method="q4_k_m")

print("Done.")
```

### Run Training

```bash
cd /home/kali/Desktop
source unsloth_env/bin/activate
python3 train.py
```

Training output:

```
Training on 247 examples...
Step 1/185 | Loss: 2.34
Step 2/185 | Loss: 2.12
...
Step 185/185 | Loss: 0.87
LoRA adapter saved to: atlas_lora/
Done.
```

## Step 5: Export Your Model

### Option A: Export to GGUF (for Ollama)

Uncomment the GGUF line in `train.py`, or run after training:

```python
model.save_pretrained_gguf("atlas_gguf", tokenizer, quantization_method="q4_k_m")
```

Then load in Ollama:

```bash
ollama create atlas-engine -f atlas_gguf/Modelfile
ollama run atlas-engine
```

### Option B: Export to vLLM

```python
model.save_pretrained_merged("atlas_merged", tokenizer, save_method="merged_16bit")
```

Then serve:

```bash
vllm serve atlas_merged
```

### Option C: Push to HuggingFace

```python
model.push_to_hub_merged(
    "your-username/atlas-engine-finetuned",
    tokenizer,
    save_method="merged_16bit",
    token="hf_your_token",
)
```

## Step 6: Use Your Fine-Tuned Model in Atlas

After exporting to Ollama, update `atlas_engine/chat.py` line 42:

```python
BACKENDS = {
    "gemini": "gemini-2.5-flash",
    "gpt": "gpt-4o-mini",
    "groq": "openai/gpt-oss-20b",
    "ollama": "atlas-engine",        # <-- your fine-tuned model
}
```

Then:

```python
from atlas_engine import Atlas
atlas = Atlas()
atlas.chat(backend="ollama")   # now uses your fine-tuned model
```

## Quick Reference

| Task | Command |
|---|---|
| Generate training data | `atlas.chat(backend="groq")` (conversations auto-logged) |
| Check training data | `wc -l chat_history/*.jsonl` |
| Merge session files | `cat chat_history/session_*_chatml.jsonl > chat_history/training_data.jsonl` |
| Install Unsloth | `pip install unsloth` (in separate venv) |
| Train | `python3 train.py` |
| Export to GGUF | `model.save_pretrained_gguf("atlas_gguf", tokenizer, quantization_method="q4_k_m")` |
| Export to vLLM | `model.save_pretrained_merged("atlas_merged", tokenizer, save_method="merged_16bit")` |
| Load in Ollama | `ollama create atlas-engine -f atlas_gguf/Modelfile` |

## Changing the Base Model

In `train.py`, change this line:

```python
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/llama-3.1-8b-instruct-bnb-4bit",  # <-- change this
```

Popular options:

| Model | model_name | VRAM |
|---|---|---|
| Llama 3.1 8B | `unsloth/llama-3.1-8b-instruct-bnb-4bit` | 6 GB |
| Gemma 2 9B | `unsloth/gemma-2-9b-it-bnb-4bit` | 6.5 GB |
| Mistral 7B | `unsloth/mistral-7b-instruct-v0.3-bnb-4bit` | 5 GB |
| Qwen 2.5 7B | `unsloth/Qwen2.5-7B-Instruct-bnb-4bit` | 5 GB |
| Phi-4 14B | `unsloth/phi-4-bnb-4bit` | 8.5 GB |
| Llama 3.3 70B | `unsloth/Llama-3.3-70B-Instruct-bnb-4bit` | 42 GB |

## Changing the Chat Template

If you use a non-Llama model, change the `chat_template` in `train.py`:

```python
tokenizer = get_chat_template(
    tokenizer,
    chat_template="llama-3.1",  # <-- change this to match your model
```

| Model Family | chat_template |
|---|---|
| Llama 3.x | `llama-3.1` |
| Mistral | `mistral` |
| Gemma | `gemma` |
| Qwen 2.5 | `qwen-2.5` |
| Phi-4 | `phi-4` |
| ChatML (generic) | `chatml` |

## VRAM Not Enough?

Reduce batch size and sequence length in `train.py`:

```python
args=SFTConfig(
    per_device_train_batch_size=1,     # lower this
    ...
)

model, tokenizer = FastLanguageModel.from_pretrained(
    ...
    max_seq_length=1024,               # lower this
)
```

Or use a smaller model (3B instead of 8B).
