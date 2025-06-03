import ngrok
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Se você não configurou a variável de ambiente NGROK_AUTHTOKEN,
# descomente a linha abaixo e adicione seu token.
token = os.getenv("NGROK_AUTH_TOKEN")
ngrok.set_auth_token(token)

# Inicia um túnel para a porta 8000 usando o protocolo http
# O listener é o objeto que gerencia o túnel
try:
    listener = ngrok.connect(8000)  # Você pode especificar o protocolo, ex: proto="tcp"
    print(f"Ingresso estabelecido em: {listener.url()}")
    print("Pressione Ctrl+C para sair.")
    # Mantenha o script em execução para manter o túnel ativo
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nFechando o túnel ngrok...")
    ngrok.disconnect(listener.url())
    ngrok.kill()
    print("Túnel fechado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
    ngrok.kill() # Garante que o processo ngrok seja finalizado em caso de erro