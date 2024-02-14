import threading
from models.cli_chat import CliChatSocket

def iniciaChat():
  endereco_local = (input("IP local: "), int(input("Porta: ")))
  endereco_destino = (input("IP destino: "), int(input("Porta: ")))

  servidor = CliChatSocket(endereco_local, endereco_destino)

  thread_servidor = threading.Thread(target=servidor.iniciar)
  thread_servidor.daemon = True
  thread_servidor.start()

  thread_servidor.join() # Caso a thread seja interrompida

if __name__ == "__main__":
  iniciaChat()
