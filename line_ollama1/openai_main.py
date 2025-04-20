import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate"  # 確保你的 Ollama 在這個端口運行


def ask_ollama(prompt):
    payload = {"model": "llama3.1", "prompt": prompt, "stream": False}
    response = requests.post(OLLAMA_API_URL, json=payload)

    if response.status_code == 200:
        return response.json().get("response", "Ollama 沒有回應")
    else:
        return "發生錯誤，請稍後再試"
