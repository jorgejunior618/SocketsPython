import threading
from cli_chat import CliChatSocket

def iniciaChat():
  endereco_local = (input("IP local: "), int(input("Porta: ")))
  endereco_envio =  (input("IP destino: "), int(input("Porta: ")))

  servidor = CliChatSocket(endereco_local, endereco_envio)

  thread_servidor = threading.Thread(target=servidor.iniciar)
  thread_servidor.daemon = True
  thread_servidor.start()

  thread_servidor.join() # Aguardar até que as threads terminem (isso não deve acontecer)

if __name__ == "__main__":
  iniciaChat()
