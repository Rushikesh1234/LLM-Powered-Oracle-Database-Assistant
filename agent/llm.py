import requests
import re

def generate_sql(schema: str, question: str, model: str = "llama3.2-oracle"):
    with open("prompt_template.txt") as f:
        template = f.read()

    prompt = template.format(schema=schema, question=question)

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False
        })

        if response.ok:
            raw_output = response.json()["response"].strip()
            return raw_output
        else:
            raise Exception("LLM error: " + response.text)
    except requests.exceptions.RequestException as e:
        raise Exception(f"LLM Connection Error: {e}")
