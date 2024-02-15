import threading
from models.cli_tabuleiro import CliTabuleiroSocket

def iniciaJogo():
  # endereco_local = (input("IP local: "), int(input("Porta: ")))
  endereco_local = ('localhost', int(input("Porta: ")))
  # endereco_destino = (input("IP destino: "), int(input("Porta: ")))
  endereco_destino = ('localhost', int(input("Porta: ")))

  sockJogo = CliTabuleiroSocket(endereco_local, endereco_destino)

  print(" Instruções:")
  print(" - Caso você inicie a partida:")
  print("     Digite \"1\" e seu adversário deverá digitar \"2\"")
  print(" - Caso seu adversário inicie a partida:")
  print("     Digite \"2\" e seu adversário deverá digitar \"1\"")

  while True:
    turnoLocal = sockJogo.definirTurno()
    turnoAdversario = sockJogo.receberTurno()

    while turnoLocal == turnoAdversario:
      print(" Defina com seu colega pelo chat quem irá iniciar a partida")
      turnoLocal = sockJogo.definirTurno()
      turnoAdversario = sockJogo.receberTurno()
    
    if turnoLocal == 1:
      print("\n Você iniciará a partida\n")
      sockJogo.iniciarJogador1()
    else:
      print("\n Aguarde o lance do seu adversário\n")
      sockJogo.iniciarJogador2()

if __name__ == "__main__":
  iniciaJogo()
