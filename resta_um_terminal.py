# Funções de interface de terminal
def instrucoes():
  print("Instruções para jogar:")
  print("  Digite a linha junto da coluna da peça que deseja mover")
  print("  Digite a linha junto da coluna da peça que deseja retirar")
  print("  - Ex. c4 d4\n")
  print("  O resultado do jogo é decidido segundo as seguintes regras:")
  print("  - Vence quem fizer o movimento que deixa apenas uma peça no tabuleiro")
  print("  - Caso não haja mais movimentos válidos, o último a ter feito um movimento perde")

def imprimeTabuleiro(tabuleiro):
  linhas = ["","a", "b", "c", "d", "e", "f", "g",""]
  print("   "," ".join(["1","2","3","4","5","6","7"]))
  for i in range(9):
    print(linhas[i], " ".join(tabuleiro[i]))

def reiniciaTabuleiro() -> list[list[str]]:
  '''# recebeMovimento
  Função que retorna um novo tabuleiro de Resta Um

  ## Retorna:
  tabuleiro : list[list[str]]
      objeto que representa um novo tabuleiro com a posição inicial do jogo

  '''
  tabuleiro = []
  posicoes = 9

  for i in range(posicoes):
    linha = []
    for j in range(posicoes):
      peca = '*'
      if i == 0 or i == 8 or j == 0 or j == 8:
        peca = ' '
      elif (i < 3 or i > 5) and (j < 3 or j > 5):
        peca = ' '
      if (i == j == 4):
        peca = 'O'
      linha.append(peca)
    tabuleiro.append(linha)

  return tabuleiro

def estaNoFim(tabuleiro: list[list[str]]) -> tuple[bool, int]:
  '''# movimentoValido

  Função que verifica e retorna se o tabuleiro ainda possui movimentos a serem realizados,
  quantas peças faltaram ser removidas caso não

  ## Parâmetros:
  tabuleiro : list[list[str]]
      objeto que representa o tabuleiro do jogo atual

  ## Retorna:
  out : tuple[ fimDeJogo : bool, contagem : int ]
      onde: [fimDeJogo] indica se há movimentos válidos e [contagem] a quantidade de peças restantes em caso de fimDeJogo[True] e 0 em caso de fimDeJogo[False]
  '''
  contagemPecas = 0
  for i in range(9):
    linha = "".join(tabuleiro[i])
    contagemPecas += linha.count('*')
    coluna = "".join(tabuleiro[:][i])
    if (linha.find("**O") != -1) or (linha.find("O**") != -1):
      return False, 0
    if (coluna.find("**O") != -1) or (coluna.find("O**") != -1):
      return False, 0
  return True, contagemPecas

# Funções relacionadas aos movimentos e validadações do jogo

def recebeMovimento() -> list[list[int]]:
  '''# recebeMovimento
  Função que recebe o input do usuário e retorna os indices indicados

  ## Retorna:
  mover : list[int]
      indice da peça que será movida de posição
  retirar : list[int]
      indice da peça que será removida do tabuleiro
  '''

  movimento = input()
  indiceLinha = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7}
  mover, retirar = movimento.split(' ')

  mover = [*mover]
  mover[0] = indiceLinha[mover[0]]
  mover[1] = int(mover[1])

  retirar = [*retirar]
  retirar[0] = indiceLinha[retirar[0]]
  retirar[1] = int(retirar[1])
  return mover, retirar

def movimentoValido(mover: list[int], retirar: list[int], tabuleiro: list[list[str]]) -> tuple[bool, list[int]]:
  '''# movimentoValido

  Função que valida se o movimento recebido nos parâmetros é válido e retorna
  o destino da peça que será movida:

  ## Parâmetros:
  mover : list[int]
      indice da peça que será movida de posição
  retirar : list[int]
      indice da peça que será removida do tabuleiro
  tabuleiro : list[list[str]]
      objeto que representa o tabuleiro do jogo atual

  ## Retorna:
  out : tuple[ valido : bool, destino : list[int] ]
      onde: [valido] indica se o movimento recebido pode ser realizado ou não e [destino] é o indice para o qual a peça [mover] deverá ir
  '''
  moverLinha, moverColuna = mover
  retirarLinha, retirarColuna = retirar

  # Verificando se as posições estão dentro do tabuleiro
  if moverLinha > 7 or moverColuna > 7 or retirarLinha > 7 or retirarColuna > 7 or moverLinha < 1 or moverColuna < 1 or retirarLinha < 1 or retirarColuna < 1:
    return False, []

  # Verificando se as posições selecionadas são peças
  if tabuleiro[moverLinha][moverColuna] != '*':
    return False, []
  if tabuleiro[retirarLinha][retirarColuna] != '*':
    return False, []

  # Caso o movimento seja Horizontal
  if moverLinha == retirarLinha:
    if moverColuna == retirarColuna or abs(moverColuna - retirarColuna) != 1: # Caso as peças selecionadas sejam identicas
      return False, []
    # Caso seja um movimento da esquerda para a direita (->)
    if moverColuna < retirarColuna:
      if tabuleiro[retirarLinha][retirarColuna+1] != 'O':
        return False, []
      return True, [retirarLinha,retirarColuna+1]
    # Caso seja um movimento da direita para a esquerda (<-)
    else:
      if tabuleiro[retirarLinha][retirarColuna-1] != 'O':
        return False, []
      return True, [retirarLinha,retirarColuna-1]

  # Caso o movimento seja Vertical
  elif moverColuna == retirarColuna:
    if moverLinha == retirarLinha or abs(moverLinha - retirarLinha) != 1: # Caso as peças selecionadas sejam identicas
      return False, []
    # Caso seja um movimento de cima para baixo (\/)
    if moverLinha < retirarLinha:
      if tabuleiro[retirarLinha+1][retirarColuna] != 'O':
        return False, []
      return True, [retirarLinha+1,retirarColuna]
    # Caso seja um movimento de baixo para cima (/\)
    else:
      if tabuleiro[retirarLinha-1][retirarColuna] != 'O':
        return False, []
      return True, [retirarLinha-1,retirarColuna]
  # Caso as peças não estajam juntas
  else:
    return False, []

def fazMovimento(mover: list[int], retirar: list[int], destino: list[int], tab: list[list[str]]):
  '''# fazMovimento

  Função recebe o movimento desejado e retorna o tabuleiro com a jogada realizada:

  ## Parâmetros:
  mover : list[int]
      indice da peça que será movida de posição
  retirar : list[int]
      indice da peça que será removida do tabuleiro
  destino : list[int]
      indice de para onde a peça [mover] deverá ir
  tab : list[list[str]]
      objeto que representa o tabuleiro do jogo atual

  ## Retorna:
  tabuleiro : list[list[str]]
      objeto que representa o tabuleiro com a nova posição depois de ser realizaada a jogada
  '''
  tabuleiro = []
  for i in range(9):
    linha = []
    for j in range(9):
      linha.append(tab[i][j])
    tabuleiro.append(linha)

  tabuleiro[mover[0]][mover[1]], tabuleiro[retirar[0]][retirar[1]], tabuleiro[destino[0]][destino[1]] = 'O','O' ,'*'

  return tabuleiro

def iniciaJogo():
  turno = 1
  tabuleiro = reiniciaTabuleiro()

  instrucoes()
  fimDeJogo, contagem = estaNoFim(tabuleiro)
  while not fimDeJogo:
    turno = 1 - turno
    imprimeTabuleiro(tabuleiro)
    print(f"Vez do Jogador {turno + 1}, Faça um movimento")
    mover, retirar = recebeMovimento()
    valido, destino = movimentoValido(mover, retirar, tabuleiro)
    while not valido:
      print("Movimento inválido, tente novamente")
      mover, retirar = recebeMovimento()
      valido, destino = movimentoValido(mover, retirar, tabuleiro)

    tabuleiro = fazMovimento(mover, retirar, destino, tabuleiro)
    fimDeJogo, contagem = estaNoFim(tabuleiro)
  print("\nFim de jogo!\n")
  imprimeTabuleiro(tabuleiro)
  if contagem > 1:
    print(f"\nPeças restantes: {contagem}")
    print(f"O vencedor é do jogador {2 - turno}\n")
  else:
    print(f"Parabens restou {contagem}!")
    print(f"O vencedor é do jogador {turno + 1}\n")

if __name__ == "__main__":
  iniciaJogo()