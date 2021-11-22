import pygame
import random
from pygame import time

pygame.init()

# ----- Gera tela principal
largura = 700
altura = 600
window = pygame.display.set_mode((largura, altura)) #tamanho da tela
pygame.display.set_caption('Fox Supremacy') #nome do jogo

# ----- Inicia estruturas de dados
game = True

# ----- Inicia assets

altura_jacare = 75
largura_jacare = 80
altura_fox = 75
largura_fox = 80
#C:/Users/lucas/Documents/Insper/1Semestre/Dessoft 2021.2/github/projetofinalpygame/ 
fundo_de_tela = pygame.image.load('imagens/fundo.png').convert_alpha()
fundo_de_tela = pygame.transform.scale(fundo_de_tela, (largura, altura))
fundo_de_tela2 = pygame.image.load('imagens/fundo.png').convert_alpha()
fundo_de_tela2 = pygame.transform.scale(fundo_de_tela, (largura, altura))
fox_imagem = pygame.image.load('imagens/fox1.png').convert_alpha()
fox_imagem = pygame.transform.scale(fox_imagem, (largura_fox, altura_fox))
jacare_imagem = pygame.image.load('imagens/jacare.png').convert_alpha()
jacare_imagem = pygame.transform.scale(jacare_imagem, (largura_jacare, altura_jacare))

# variaveis globais
x=0

# ----- Inicia estruturas de dados
# Definindo os novos tipo
class Fox(pygame.sprite.Sprite): #classe da raposa
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img 
        self.rect = self.image.get_rect()
        self.rect.centerx = 300 #possição raposa eixo x
        self.rect.bottom = 550 #posição raposa eixo y
        self.speedx = 0
        self.speedy = 0

    def update(self):
        # Atualização da posição da raposa
        self.rect.centerx += self.speedx
        self.rect.bottom += self.speedy

        # Mantem dentro da tela
        if self.rect.right > largura:
            self.rect.right = largura #mantem na tela
        if self.rect.left < 0:
            self.rect.left = 0 #mantem na tela
        if self.rect.bottom<350: #quando pula
            self.speedy=3 #cai com velocidade 5
        if self.rect.bottom>550: # quando pula demais
            self.rect.bottom=550 #volta para o chão

class Jacare(pygame.sprite.Sprite): #classe do jacaré
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = 700 + largura_jacare
        self.rect.bottom = 550
        self.speedx = random.randrange(-5.0, -2.0) #move o jacaré junto com a tela
        self.speedy = 0

    def update(self):
        # Atualização da posição do jacaré
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.left < -largura_jacare:
            self.rect.x = random.randint(700+largura_jacare, 1400)
            



clock = pygame.time.Clock()
FPS = 60

jogador = Fox(fox_imagem)
inimigo = Jacare(jacare_imagem)

todos_objetos = pygame.sprite.Group()
grupo_jacare = pygame.sprite.Group()
grupo_jacare.add(inimigo)
todos_objetos.add(inimigo)
todos_objetos.add(jogador)


# ===== Loop principal =====
while game:

    clock.tick(FPS)


    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False #para sair do jogo
                     #para pular
        if event.type == pygame.KEYDOWN:
            if jogador.rect.bottom >= 550:
                if event.key == pygame.K_UP:
                    jogador.speedy=-4 #faz a raposa subir com 5 de velocidade
            if event.key == pygame.K_RIGHT: 
                jogador.speedy=0
        
        '''TEM QUE ARRUMAR ESSA PARTE AQUI DE CIMA PORQUE ANTES TODAS TECLAS AVAM PRS PULAR E AGORA NAO PULA'''

    # atualiza posição ( por enquanto zerada)
    todos_objetos.update()

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor branca
    window.blit(fundo_de_tela, (x, 0))
    window.blit(fundo_de_tela2, ((700+x), 0)) #anda o fundo da tela
    window.blit(jogador.image, jogador.rect)
    todos_objetos.draw(window)

    hits = pygame.sprite.spritecollide(jogador, grupo_jacare, True)
    if len(hits)>0:
        game = False

    # ------- Fundo infinito
    if x <= -700:
        x = 0
    else:
        x-=2
    

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

 #para o fundo andar no sentido correto

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
