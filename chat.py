import threading
from models.cli_chat import CliChatSocket

def iniciaChat():
  endereco_local = ('localhost', 4321)
  endereco_destino = ('localhost', 1234)

  chat = CliChatSocket(endereco_local, endereco_destino)

  thread_chat = threading.Thread(target=chat.iniciar)
  thread_chat.daemon = True
  thread_chat.start()

  thread_chat.join() # Caso a thread seja interrompida

if __name__ == "__main__":
  iniciaChat()
