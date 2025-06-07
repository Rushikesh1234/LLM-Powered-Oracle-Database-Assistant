
# 🧠 LLM-Powered Oracle Database Assistant

This project is a full-stack AI assistant designed to generate and execute **Oracle SQL queries** using a **fine-tuned LLM (LLaMA 3.2)**. It features a natural language interface (via Streamlit) where users can ask questions in plain English, and the model returns the corresponding Oracle SQL query and its results.

---

## 🚀 Features

- 🔍 **Natural Language to SQL**: Converts English questions into Oracle SQL queries.
- 🧠 **Fine-Tuned LLaMA Model**: Custom-trained for enterprise Oracle DB understanding.
- 🖥️ **Streamlit Interface**: Simple, interactive UI for querying.
- 🗃️ **Live Oracle DB Execution**: Executes queries and shows results.
- ⚙️ **Modular Backend**: Cleanly separated model, DB, and UI logic.
- 📦 **Offline Model Support**: Uses `llama.cpp` for efficient on-device inference.

---

## 🗂️ Project Structure

```bash
LLM-Powered-Oracle-Database-Assistant/
│
├── agent/                        # Main model interaction script
│   ├── app.py
│   ├── db.py
│   ├── llm.py
│   ├── promp_template.txt
│   ├── streamlit_app.py         # Streamlit frontend
│   ├── test_connect_oracle.py
│   └── requirements.txt
│
├── fine-tune-agent/             # Fine-tuning pipeline and outputs
│   ├── llama.cpp/               # llama.cpp backend
│   ├── llama3.2-oracle/         # Original fine-tuned GGUF model
│   ├── merged_model/            # Merged final model
│   ├── trained_model/           # PEFT adapter model
│   ├── outputs/                 # Training checkpoints
│   ├── myenv/                   # Virtual environment
│   ├── oracle_training_dataset.jsonl
│   ├── train_model.py
│   ├── merged_model.py
│   └── requirements.txt
```

---

## 🧑‍💻 Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/Rushikesh1234/LLM-Powered-Oracle-Database-Assistant.git
cd LLM-Powered-Oracle-Database-Assistant
```

### 2. Set Up Environment

#### For Oracle DB Access:
- Make sure you have an Oracle client (like `cx_Oracle` or `oracledb`) installed.
- Update your DB connection string in `db.py`.

#### For LLM Inference:
- Use `llama.cpp` to run the `LLMA_Oracle_model.gguf` (or switch to the merged model).

```bash
cd fine-tune-agent/llama.cpp
make
./main -m ../llama3.2-oracle/LLMA_Oracle_model.gguf
```

### 3. Install Dependencies
```bash
cd agent
pip install -r requirements.txt
```

### 4. Run Streamlit App
```bash
streamlit run streamlit_app.py
```

---

## 🏋️ Fine-Tuning

The LLM was fine-tuned using Oracle-specific SQL queries via PEFT and LORA. Training script and dataset are available in:

```bash
fine-tune-agent/train_model.py
fine-tune-agent/oracle_training_dataset.jsonl
```

---

## 📄 Sample Prompt Template

```txt
You are an Oracle SQL assistant. Based on the following database schema, generate a valid SQL query.
Only return the raw Oracle SQL, with no explanation and no markdown formatting. Only output a valid SQL query, nothing else.

Schema:
{schema}

Question:
{question}

SQL:
```

---

## 📸 Demo Screenshot

![Demo Video for SQL Select Query Execution](https://github.com/user-attachments/assets/6e5dde96-7826-49e2-80ca-669b24320563)

---
