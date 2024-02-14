import threading
from models.cli_tabuleiro import CliTabuleiroSocket

def iniciaJogo():
  # endereco_local = (input("IP local: "), int(input("Porta: ")))
  endereco_local = ('localhost'), int(input("Porta: "))
  # endereco_destino = (input("IP destino: "), int(input("Porta: ")))
  endereco_destino = ('localhost'), int(input("Porta: "))

  servidor = CliTabuleiroSocket(endereco_local, endereco_destino)

  thread_servidor = threading.Thread(target=servidor.iniciar)
  thread_servidor.daemon = True
  thread_servidor.start()

  thread_servidor.join() # Caso a thread seja interrompida

if __name__ == "__main__":
  iniciaJogo()
