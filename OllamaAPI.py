import requests
import json

def chat_ollama_stream(prompt, model="llama2:latest", max_tokens=200, temperature=0.7):
    """
    Envia uma solicitação ao modelo via API Ollama usando o endpoint /api/generate.
    Retorna uma resposta formatada em tempo real para o app principal.

    Args:
        prompt (str): Pergunta ou comando enviado ao modelo.
        model (str): Nome do modelo. Padrão é 'llama2:latest'.
        max_tokens (int): Máximo de tokens na resposta.
        temperature (float): Aleatoriedade das respostas.

    Returns:
        str: Resposta gerada pelo modelo.
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": True  # Habilita o streaming
    }

    response_text = ""
    try:
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()

        for chunk in response.iter_lines():
            if chunk:
                data = chunk.decode("utf-8")
                try:
                    chunk_data = json.loads(data)  # Converte o JSON em um dicionário
                    if "response" in chunk_data:
                        # Concatena a resposta progressivamente
                        response_text += chunk_data["response"]
                    if chunk_data.get("done", False):
                        break
                except json.JSONDecodeError as e:
                    response_text += f"[Erro ao processar chunk: {e}]"

    except requests.exceptions.RequestException as e:
        response_text = f"Erro na conexão com o servidor Ollama: {str(e)}"

    return response_text
