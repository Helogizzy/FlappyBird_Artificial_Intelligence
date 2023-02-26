import pygame  #Biblioteca de criar jogos
import os  #Bibliotea para integrar o codigo com os arquivos do computador (imagens, etc)
import random  #Geracao de numeros aleatorios, utilizada para a geracao da posicao dos canos
from agbird import Individuo, Populacao
#Variaveis Constantes
TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_CANO = pygame.transform.scale2x(
  pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(
  pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(
  pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGENS_PASSARO = [
  pygame.transform.scale2x(pygame.image.load(os.path.join('imgs',
                                                          'bird1.png'))),
  pygame.transform.scale2x(pygame.image.load(os.path.join('imgs',
                                                          'bird2.png'))),
  pygame.transform.scale2x(pygame.image.load(os.path.join('imgs',
                                                          'bird3.png'))),
]


#Criando os objetos do jogo (o que s movimenta no jogo)
class Passaro:
  IMGS = IMAGENS_PASSARO.copy()
  #animação da rotação
  ROTACAO_MAXIMA = 25
  VELOCIDADE_ROTACAO = 20
  TEMPO_ANIMACAO = 5

  def __init__(self, x, y, individuo : Individuo = None):
    self.x = x
    self.y = y
    self.angulo = 0
    self.velocidade = 0
    self.altura = self.y
    self.tempo = 0  #Utilizada para o tempo de "descida" do passaro
    self.contagem_imagem = 0  #Utilizada para verificar qual imagem do passaro está sendo usada
    self.imagem = self.IMGS[0]
    self.individuo = individuo

  #Função pular do passaro
  def pular(self):
    self.velocidade = -10.5 
    self.tempo = 0  #=0 pois quando o passaro pula ele só se desloca no eixo y
    self.altura = self.y

  #Função de mover o passaro
  def mover(self):
    #Calcular o deslocamento
    self.tempo += 1
    deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

    #Restringir o deslocamento
    if deslocamento > 16:
      deslocamento = 16
    elif deslocamento < 0:
      deslocamento -= 2

    self.y += deslocamento

    #Angulo do passaro
    if deslocamento < 0 or self.y < (self.altura + 50):
      if self.angulo < self.ROTACAO_MAXIMA:
        self.angulo = self.ROTACAO_MAXIMA
    else:
      if self.angulo > -90:
        self.angulo -= self.VELOCIDADE_ROTACAO

  #Fução de desenhar
  def desenhar(self, tela):
    #Definir qual imagem do passaro vai usar
    self.contagem_imagem += 1

    if self.contagem_imagem < self.TEMPO_ANIMACAO:
      self.imagem = self.IMGS[0]

    elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
      self.imagem = self.IMGS[1]

    elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
      self.imagem = self.IMGS[2]

    elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:
      self.imagem = self.IMGS[1]

    elif self.contagem_imagem >= self.TEMPO_ANIMACAO * 4 + 1:
      self.imagem = self.IMGS[0]
      self.contagem_imagem = 0

    #Se o passaro tiver caindo nao bate a asa
    if self.angulo <= -80:
      self.imagem = self.IMGS[1]
      self.contagem_imagem = self.TEMPO_ANIMACAO * 2

    #Desenhar a imagem
    imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
    pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
    retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
    tela.blit(imagem_rotacionada, retangulo.topleft)

  #Função para pegar a mascara do passaro e do cano, para verificar se o passaro bateu no cano
  def get_mask(self):
    return pygame.mask.from_surface(self.imagem)


#Função do cano
class Cano:
  #Contantes
  DISTANCIA = 200
  VELOCIDADE = 5

  def __init__(self, x):
    self.x = x
    self.altura = 0
    self.pos_topo = 0
    self.pos_base = 0
    self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
    self.CANO_BASE = IMAGEM_CANO
    self.passou = False
    self.definir_altura()

  def definir_altura(self):
    self.altura = random.randrange(50, 450)
    self.pos_topo = self.altura - self.CANO_TOPO.get_height()
    self.pos_base = self.altura + self.DISTANCIA

  #Função de mover o cano
  def mover(self):
    self.x -= self.VELOCIDADE

  #Função de desenhar o cano
  def desenhar(self, tela):
    tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
    tela.blit(self.CANO_BASE, (self.x, self.pos_base))

  #Função para pegar a marcara do cano e verificar se o passaro colidiu com o cano
  def colidir(self, passaro):
    passaro_mask = passaro.get_mask()
    topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
    base_mask = pygame.mask.from_surface(self.CANO_BASE)

    distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
    distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

    topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
    base_ponto = passaro_mask.overlap(base_mask, distancia_base)

    if base_ponto or topo_ponto:
      return True
    else:
      return False


#Função do chão
class Chao:
  VELOCIDADE = 5
  LARGURA = IMAGEM_CHAO.get_width()
  IMAGEM = IMAGEM_CHAO

  def __init__(self, y):
    self.y = y
    self.x1 = 0
    self.x2 = self.LARGURA

  def mover(self):
    self.x1 -= self.VELOCIDADE
    self.x2 -= self.VELOCIDADE

    if self.x1 + self.LARGURA < 0:
      self.x1 = self.x2 + self.LARGURA
    if self.x2 + self.LARGURA < 0:
      self.x2 = self.x1 + self.LARGURA

  def desenhar(self, tela):
    tela.blit(self.IMAGEM, (self.x1, self.y))
    tela.blit(self.IMAGEM, (self.x2, self.y))


#Função para desenhar a tela do jogo
def desenhar_tela(tela, passaros, canos, chao, pontos):
  pygame.font.init()
  FONTE_PONTOS = pygame.font.SysFont('arial', 50)
  tela.blit(IMAGEM_BACKGROUND, (0, 0))
  for passaro in passaros:
    passaro.desenhar(tela)
  for cano in canos:
    cano.desenhar(tela)

  texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
  tela.blit(texto, (0, 0))
  chao.desenhar(tela)
  pygame.display.update()


#Função principal
populacao_inicial = Populacao(30)

passaros = []
for individuo in populacao_inicial.individuos:
  passaro_novo = Passaro(230, 350)
  passaro_novo.individuo = individuo
  passaros.append(passaro_novo)

def main():
  VELOCIDADE_CANOS = 4
  chao = Chao(730)
  canos = [Cano(700)]
  tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
  pontos = 0
  relogio = pygame.time.Clock()
  distancia = 0
  #Colocando o jogo para rodar
  rodando = True

  #Laço Máquina de Estados
  while rodando:
    relogio.tick(30)  #frames

    #Interação com o jogo
    #Finaliza o jogo.
    if len(passaros) <= 0:
      rodando = False
      pygame.quit()
      break

    for evento in pygame.event.get():
      if evento.type == pygame.QUIT:
        rodando = False
        pygame.quit()
        quit()

    #Mover as coisas
    for passaro in passaros:
      passaro.mover()
      distancia += 1
      if canos[-1].x < TELA_LARGURA:
        distancia_basey = [passaro.y-canos[-1].pos_base]
        distancia_topoy = [passaro.y-canos[-1].pos_topo]
      else:
        distancia_basey = [passaro.y-canos[0].pos_base]
        distancia_topoy = [passaro.y-canos[0].pos_topo]
      if passaro.individuo.pular([distancia_basey, distancia_topoy]):
        passaro.pular()
    chao.mover()

    #Canos
    adicionar_cano = False
    remover_canos = []
    for cano in canos:
      for i, passaro in enumerate(passaros):
        if cano.colidir(passaro):
          passaros.pop(i)
        if not cano.passou and passaro.x > cano.x:
          cano.passou = True
          adicionar_cano = True
      cano.mover()
      if cano.x + cano.CANO_TOPO.get_width() < 0:
        remover_canos.append(cano)

    #Adição de canos
    if adicionar_cano:
      pontos += 1
      canos.append(Cano(600))
      canos[-1].VELOCIDADE = VELOCIDADE_CANOS
        
      # Máquina de Estado
      # Estado 01: incrementando pontos até chegar em 5
      if pontos == 5: 
          # Estado 02: aumenta a velocidade
          VELOCIDADE_CANOS += 4
          canos[-1].VELOCIDADE = VELOCIDADE_CANOS
            
          # Estado 03: zera os pontos e retorna para o 1º estado para a recontagem
          pontos = 0

    for cano in remover_canos:
      canos.remove(cano)
    #Verifica se o passaro saiu da tela, se sim ele morre
    for i, passaro in enumerate(passaros):
      passaros[i].individuo.fitness=distancia
      if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
        # print(f"Passáro {i} recebeu {pontos}")
        # print(f"Quantidade {len(passaros)}")
        passaros.pop(i)

    desenhar_tela(tela, passaros, canos, chao, pontos)


#Execução
if __name__ == '__main__':
  for i in range(100):
    main()
    selecionados = populacao_inicial.selecao()
    print(f"Selecionados {i}")
    elites = populacao_inicial.get_elite() + populacao_inicial.get_elite()
    populacao_inicial = selecionados.animal_crossing(elite=elites)
    print(f"Geração {i}")
    for individuo in populacao_inicial.individuos:
      passaro_novo = Passaro(230, 350)
      passaro_novo.individuo = individuo
      passaros.append(passaro_novo)