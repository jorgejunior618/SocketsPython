class JogoRestaUm:
  def __init__(self):
    self.tabuleiro = []
    self.turno = 0

  def reiniciaTabuleiro(self) -> list[list[str]]:
    '''# reiniciaTabuleiro
    Função que retorna um novo tabuleiro de Resta Um

    ## Retorna:
    tabuleiro : list[list[str]]
        objeto que representa um novo tabuleiro com a posição inicial do jogo

    '''
    self.turno = 0
    self.tabuleiro = []
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
      self.tabuleiro.append(linha)

  def estaNoFim(self) -> tuple[bool, int]:
    '''# estaNoFim

    Função que verifica e retorna se o tabuleiro ainda possui movimentos a serem realizados,
    quantas peças faltaram ser removidas caso não

    ## Retorna:
    out : tuple[ fimDeJogo : bool, contagem : int ]
        onde: [fimDeJogo] indica se há movimentos válidos e [contagem] a quantidade de peças restantes em caso de fimDeJogo[True] e 0 em caso de fimDeJogo[False]
    '''
    contagemPecas = 0
    for i in range(9):
      linha = "".join(self.tabuleiro[i])
      contagemPecas += linha.count('*')
      coluna = "".join([lin[i] for lin in self.tabuleiro])
      if (linha.find("**O") != -1) or (linha.find("O**") != -1):
        return False, 0
      if (coluna.find("**O") != -1) or (coluna.find("O**") != -1):
        return False, 0
    return True, contagemPecas

# Funções relacionadas aos movimentos e validadações do jogo
  def movimentoValido(self, mover: list[int], retirar: list[int]) -> tuple[bool, list[int]]:
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
    if self.tabuleiro[moverLinha][moverColuna] != '*':
      return False, []
    if self.tabuleiro[retirarLinha][retirarColuna] != '*':
      return False, []

    # Caso o movimento seja Horizontal
    if moverLinha == retirarLinha:
      if moverColuna == retirarColuna or abs(moverColuna - retirarColuna) != 1: # Caso as peças selecionadas sejam identicas
        return False, []
      # Caso seja um movimento da esquerda para a direita (->)
      if moverColuna < retirarColuna:
        if self.tabuleiro[retirarLinha][retirarColuna+1] != 'O':
          return False, []
        return True, [retirarLinha,retirarColuna+1]
      # Caso seja um movimento da direita para a esquerda (<-)
      else:
        if self.tabuleiro[retirarLinha][retirarColuna-1] != 'O':
          return False, []
        return True, [retirarLinha,retirarColuna-1]

    # Caso o movimento seja Vertical
    elif moverColuna == retirarColuna:
      if moverLinha == retirarLinha or abs(moverLinha - retirarLinha) != 1: # Caso as peças selecionadas sejam identicas
        return False, []
      # Caso seja um movimento de cima para baixo (\/)
      if moverLinha < retirarLinha:
        if self.tabuleiro[retirarLinha+1][retirarColuna] != 'O':
          return False, []
        return True, [retirarLinha+1,retirarColuna]
      # Caso seja um movimento de baixo para cima (/\)
      else:
        if self.tabuleiro[retirarLinha-1][retirarColuna] != 'O':
          return False, []
        return True, [retirarLinha-1,retirarColuna]
    # Caso as peças não estajam juntas
    else:
      return False, []

  def fazMovimento(self, mover: list[int], retirar: list[int], destino: list[int]):
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
    tab = []
    for i in range(9):
      linha = []
      for j in range(9):
        linha.append(self.tabuleiro[i][j])
      tab.append(linha)

    tab[mover[0]][mover[1]], tab[retirar[0]][retirar[1]], tab[destino[0]][destino[1]] = 'O','O' ,'*'

    self.turno = 1 - self.turno
    self.tabuleiro = tab

  def recebeMovimento(self, movimento: str) -> list[list[int]]:
    '''# recebeMovimento
    Função que recebe o input do usuário e retorna os indices indicados

    ## Retorna:
    mover : list[int]
        indice da peça que será movida de posição
    retirar : list[int]
        indice da peça que será removida do tabuleiro
    '''

    indiceLinha = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7}
    mover, retirar = movimento.split(' ')

    mover = [*mover]
    mover[0] = indiceLinha[mover[0]]
    mover[1] = int(mover[1])

    retirar = [*retirar]
    retirar[0] = indiceLinha[retirar[0]]
    retirar[1] = int(retirar[1])
    return mover, retirar
