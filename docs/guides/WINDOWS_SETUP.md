# Windows Setup: Atlas Engine + Unsloth Fine-Tuning

Paso a paso desde cero en Windows con PowerShell.

## Prerequisitos

- Windows 10/11
- NVIDIA GPU con drivers instalados (RTX 2060+ recomendado)
- Git instalado (https://git-scm.com/download/win)
- Python 3.12 instalado (https://python.org) -- NO uses 3.13

Verifica en PowerShell:

```powershell
git --version
python --version
nvidia-smi
```

Si `nvidia-smi` no muestra tu GPU, instala drivers de https://nvidia.com/drivers

---

## Parte 1: Clonar el Proyecto

```powershell
cd ~\Desktop
git clone https://github.com/Audionerdz/CTF-Bug-Hunter-Retrieval.git RAG
cd RAG
```

---

## Parte 2: Crear venv e instalar dependencias

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
pip install langchain-groq
```

---

## Parte 3: Copiar tus API keys

Crea la carpeta `.env` y los archivos:

```powershell
mkdir .env
```

```powershell
"OPENAI_API_KEY=tu_openai_key" | Out-File -Encoding utf8 .env\openai.env
"PINECONE_API_KEY=tu_pinecone_key" | Out-File -Encoding utf8 .env\pinecone.env
"GOOGLE_API_KEY=tu_gemini_key" | Out-File -Encoding utf8 .env\gemini.env
"GROQ_API_KEY=tu_groq_key" >> .env\openai.env
```

Reemplaza `tu_*_key` con tus keys reales. Copia los valores de tu Kali:

```bash
# En Kali, para ver tus keys:
cat /home/kali/Desktop/RAG/.env/openai.env
cat /home/kali/Desktop/RAG/.env/pinecone.env
cat /home/kali/Desktop/RAG/.env/gemini.env
```

---

## Parte 4: Verificar que Atlas funciona

```powershell
.\venv\Scripts\Activate.ps1
python
```

```python
from atlas_engine import Atlas
atlas = Atlas()
atlas.ask("What is LFI?", backend="groq")
# Si ves respuesta, todo funciona
exit()
```

---

## Parte 5: Copiar training data de Kali a Windows

### Opcion A: Via GitHub (ya esta subido)

Los archivos `chat_history/*.jsonl` ya estan en el repo. Al clonar ya los tienes.

### Opcion B: Via SCP (si tienes SSH a tu Kali)

```powershell
scp kali@tu_ip:/home/kali/Desktop/RAG/chat_history/*.jsonl .\chat_history\
```

### Opcion C: Manual

Copia los archivos `.jsonl` de `chat_history/` en tu Kali a `RAG\chat_history\` en Windows via USB o nube.

---

## Parte 6: Mergear training data

```powershell
Get-Content .\chat_history\session_*_chatml.jsonl | Out-File -Encoding utf8 .\chat_history\training_data.jsonl
```

Verificar cuantos ejemplos tienes:

```powershell
(Get-Content .\chat_history\training_data.jsonl).Count
```

---

## Parte 7: Instalar Unsloth (venv separado)

NO mezcles con el venv de Atlas. Crea uno nuevo:

```powershell
cd ~\Desktop
python -m venv unsloth_env
.\unsloth_env\Scripts\Activate.ps1
pip install --upgrade pip
```

Instala PyTorch primero (selecciona tu version de CUDA):

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

Si no sabes tu version de CUDA:

```powershell
nvidia-smi
# Mira la linea "CUDA Version: 12.x"
# Si es 12.1 usa cu121, si es 12.4 usa cu124
```

Luego instala Unsloth:

```powershell
pip install unsloth
```

Verifica:

```powershell
python -c "from unsloth import FastLanguageModel; print('Unsloth ready')"
```

---

## Parte 8: Crear script de training

Crea el archivo `train.py` en `~\Desktop\`:

```powershell
notepad ~\Desktop\train.py
```

Pega esto:

```python
from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template, standardize_sharegpt
from datasets import load_dataset
from trl import SFTTrainer, SFTConfig
import os

# =============================================
# 1. LOAD MODEL
# =============================================
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
# 3. LOAD ATLAS ENGINE DATA
# =============================================
data_path = os.path.expanduser("~\\Desktop\\RAG\\chat_history\\training_data.jsonl")
dataset = load_dataset("json", data_files=data_path, split="train")
dataset = standardize_sharegpt(dataset)

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
    dataset_num_proc=1,  # REQUIRED on Windows
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
model.save_pretrained("atlas_lora")
tokenizer.save_pretrained("atlas_lora")
print("LoRA saved to: atlas_lora/")

# Uncomment to export as GGUF for Ollama:
# model.save_pretrained_gguf("atlas_gguf", tokenizer, quantization_method="q4_k_m")
```

---

## Parte 9: Entrenar

```powershell
cd ~\Desktop
.\unsloth_env\Scripts\Activate.ps1
python train.py
```

Esto va a:
1. Descargar el modelo (~4GB la primera vez)
2. Cargar tu training data
3. Entrenar (minutos a horas dependiendo de ejemplos y GPU)
4. Guardar el LoRA adapter en `atlas_lora/`

---

## Parte 10: Exportar a GGUF para Ollama

Despues de entrenar, en el mismo script o en Python:

```powershell
.\unsloth_env\Scripts\Activate.ps1
python
```

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    "atlas_lora",
    max_seq_length=2048,
    load_in_4bit=True,
)

model.save_pretrained_gguf("atlas_gguf", tokenizer, quantization_method="q4_k_m")
print("GGUF saved to: atlas_gguf/")
```

---

## Parte 11: Cargar en Ollama (opcional)

Si tienes Ollama instalado en Windows (https://ollama.ai):

```powershell
ollama create atlas-engine -f atlas_gguf\Modelfile
ollama run atlas-engine
```

---

## Troubleshooting

### "No module named 'unsloth'"
Asegurate de estar en el venv correcto:
```powershell
.\unsloth_env\Scripts\Activate.ps1
```

### Out of Memory (OOM)
Baja el batch size en `train.py`:
```python
per_device_train_batch_size=1,
```
O usa un modelo mas pequeno:
```python
model_name="unsloth/gemma-2-2b-it-bnb-4bit",  # 2B en vez de 8B
```

### "CUDA not available"
```powershell
python -c "import torch; print(torch.cuda.is_available())"
```
Si dice `False`: reinstala PyTorch con la version correcta de CUDA.

### PowerShell no deja ejecutar scripts
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Quiero mas training data
Vuelve a Kali, chatea mas con Atlas, y copia los nuevos `.jsonl`:
```powershell
scp kali@tu_ip:/home/kali/Desktop/RAG/chat_history/*.jsonl .\RAG\chat_history\
Get-Content .\RAG\chat_history\session_*_chatml.jsonl | Out-File -Encoding utf8 .\RAG\chat_history\training_data.jsonl
```

---

## Resumen de Comandos

```
# 1. Clonar
git clone https://github.com/Audionerdz/CTF-Bug-Hunter-Retrieval.git RAG

# 2. Atlas (venv 1)
cd RAG && python -m venv venv && .\venv\Scripts\Activate.ps1
pip install -r requirements.txt && pip install langchain-groq

# 3. Unsloth (venv 2)
cd ~\Desktop && python -m venv unsloth_env && .\unsloth_env\Scripts\Activate.ps1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
pip install unsloth

# 4. Mergear data
Get-Content .\RAG\chat_history\session_*_chatml.jsonl | Out-File -Encoding utf8 .\RAG\chat_history\training_data.jsonl

# 5. Entrenar
python train.py

# 6. Exportar
python -c "from unsloth import FastLanguageModel; m,t=FastLanguageModel.from_pretrained('atlas_lora',max_seq_length=2048,load_in_4bit=True); m.save_pretrained_gguf('atlas_gguf',t,quantization_method='q4_k_m')"
```
