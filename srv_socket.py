import socket
import threading

class SrvSocket:
  def __init__(self, endereco_local):
    self.endereco_local = endereco_local
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sock.bind(endereco_local)

  def receber_mensagens(self):
    while True:
      dados, endereco = self.sock.recvfrom(1024)
      print(f"\n[{endereco}]: {dados.decode()}", end="\n>")

  def enviar_mensagem(self, endereco_destino):
    while True:
      mensagem = input(">")
      self.sock.sendto(mensagem.encode(), endereco_destino)

  def iniciar(self, endereco_destino):
    thread_recebimento = threading.Thread(target=self.receber_mensagens)
    thread_recebimento.daemon = True
    thread_recebimento.start()
    self.enviar_mensagem(endereco_destino)

def main():
  endereco_local_servidor = ('localhost', 12345)
  endereco_local_cliente = ('localhost', 54321)

  servidor = SrvSocket(endereco_local_servidor)

  # endereco_destino_cliente = ('localhost', 12345)

  # Iniciar servidor e cliente em threads separadas
  thread_servidor = threading.Thread(target=servidor.iniciar, args=(endereco_local_cliente,))
  thread_servidor.daemon = True
  thread_servidor.start()

  # Aguardar até que as threads terminem (isso não deve acontecer)
  thread_servidor.join()

if __name__ == "__main__":
  main()
