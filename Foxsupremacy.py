#----------------Importa bibliotecas UTILIZADAS
from typing import Final
import pygame
import random
from pygame import time
import time
import math
from ExtrairMetodo import *

pygame.init()

#----------------Gera tela principal
largura = 700
altura = 600
window = pygame.display.set_mode((largura, altura)) #tamanho da tela
pygame.display.set_caption('Fox Supremacy') #nome do jogo

#----------------Inicia estruturas de dados
game = True
inicial = True
final = True

#----------------Inicia assets
altura_jacare = 75
largura_jacare = 80 
altura_fox = 75
largura_fox = 80
altura_bala = 20
largura_bala = 30 
altura_coracao = 60
largura_coracao = 70
altura_arma = 70
largura_arma = 60

#----------------Imagens     
fundo_de_tela = pygame.image.load('imagens/fundo.png').convert_alpha()
fundo_de_tela = pygame.transform.scale(fundo_de_tela, (largura, altura))
fundo_de_tela2 = pygame.image.load('imagens/fundo.png').convert_alpha()
fundo_de_tela2 = pygame.transform.scale(fundo_de_tela, (largura, altura))
fox_imagem = pygame.image.load('imagens/fox1.png').convert_alpha()
fox_imagem = pygame.transform.scale(fox_imagem, (largura_fox, altura_fox))
fox_imagem2 = pygame.image.load('imagens/fox2.png').convert_alpha()
fox_imagem2 = pygame.transform.scale(fox_imagem2, (largura_fox, altura_fox))
fox_imagem3 = pygame.image.load('imagens/fox3.png').convert_alpha()
fox_imagem3 = pygame.transform.scale(fox_imagem3, (largura_fox, altura_fox))
fox_imagem4 = pygame.image.load('imagens/fox4.png').convert_alpha()
fox_imagem4 = pygame.transform.scale(fox_imagem4, (largura_fox, altura_fox))
jacare_imagem = pygame.image.load('imagens/jacare.png').convert_alpha()
jacare_imagem = pygame.transform.scale(jacare_imagem, (largura_jacare, altura_jacare))
bala_imagem = pygame.image.load('imagens/bala.png').convert_alpha()
bala_imagem = pygame.transform.scale(bala_imagem, (largura_bala, altura_bala))
coracao_imagem = pygame.image.load('imagens/coracao.png').convert_alpha()
coracao_imagem = pygame.transform.scale(coracao_imagem, (largura_coracao, altura_coracao))
coracao_imagem2 = coracao_imagem
coracao_imagem3 = coracao_imagem
arma_imagem = pygame.image.load('imagens/arma.png').convert_alpha()
arma_imagem = pygame.transform.scale(arma_imagem, (largura_arma, altura_arma))
fundo_inicial = pygame.image.load('imagens/inicio2.png').convert_alpha()
fundo_inicial = pygame.transform.scale(fundo_inicial, (largura, altura))
instru = pygame.image.load('imagens/instru.png').convert_alpha()
instru = pygame.transform.scale(instru, (300, 200))
fundo_final = pygame.image.load('imagens/gameover.png').convert_alpha()
fundo_final = pygame.transform.scale(fundo_final, (largura, altura))

#----------------Fontes
fonte = pygame.font.Font('imagens/fonte.ttf', 30)
fonte2 = pygame.font.Font('imagens/fonte.ttf', 50)
fonte3 = pygame.font.Font('imagens/fonte.ttf', 20)
fonte4 = pygame.font.Font('imagens/fonte.ttf', 40)

#----------------Pontos e vidas
coracoes = [coracao_imagem, coracao_imagem2, coracao_imagem3]
pontos_coracoes = [(20, 20), (90, 20), (160, 20)]
ponto_arma = (330, 15)

#----------------Para animação da raposa
fox_anim = []
for i in range(4):
    # Os arquivos de animação são numerados de 00 a 08
    filename = 'imagens/fox{}.png'.format(i+1)
    img = pygame.image.load(filename).convert_alpha()
    img = pygame.transform.scale(img, (75, 80))
    fox_anim.append(img)

#----------------Carrega o som
pygame.mixer.music.load('sons/mfundoof.wav') #musica de fundo
pygame.mixer.music.set_volume(0.4) #define o volume

#----------------Variáveis globais
x=0
contador_balas = 0
vidas = 3
aceleracao = 1
placar = 0
pausa_inicial = True
contador_mais100 = 0
cor_branco = (255, 255, 255)
cor_preto = (0,0,0)
posicao_x = 350

#----------------Inicia estruturas de dados

#==================================CLASSES==================================

#----------------Classe da raposa
class Fox(pygame.sprite.Sprite): 
    def __init__(self, img, todos_objetos, grupo_balas, bala_imagem, center):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.fox_anim = fox_anim
        self.frame = 0  # Armazena o índice atual na animação
        self.image = self.fox_anim[self.frame]  # Pega a primeira imagem
        self.rect = self.image.get_rect()
        self.rect.centerx = 300 #possição raposa eixo x
        self.rect.bottom = 550 #posição raposa eixo y
        self.speedx = 0
        self.speedy = 0
        self.todos_objetos = todos_objetos
        self.grupo_balas = grupo_balas
        self.bala_imagem = bala_imagem
        self.mask = pygame.mask.from_surface(self.image)
        self.step = 10

    def update(self):
        # Atualização da posição da raposa
        self.rect.centerx += self.speedx
        self.rect.bottom += self.speedy

        # Mantem dentro da tela
        if self.rect.right > largura:
            self.rect.right = largura #mantem na tela
        if self.rect.left < 0:
            self.rect.left = 0 #mantem na tela
        if self.rect.bottom<440: #quando pula
            self.speedy=3 #cai com velocidade 5
        if self.rect.bottom>550: # quando pula demais
            self.rect.bottom=550 #volta para o chão
        

        # Avança um quadro.
        self.frame+=1
        if self.frame>=self.step*4:
            self.frame=0
        if self.frame % self.step == 0:
            index = self.frame // 10
            center = self.rect.center
            self.image = self.fox_anim[index]
            self.rect = self.image.get_rect()
            self.rect.center = center

    def shoot(self):
        # A nova bala criada
            if contador_balas == 0:
                nova_bala = Bullet(self.bala_imagem, self.rect.bottom-25 , self.rect.centerx+44)
                self.todos_objetos.add(nova_bala)
                self.grupo_balas.add(nova_bala)        

#------------------------Fim classe da raposa------------------------------

#----------------Classe do jacaré

class Jacare(pygame.sprite.Sprite): 
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = 700 + largura_jacare
        self.rect.bottom = 550
        self.speedx = random.randrange(-5.0, -3.0)*aceleracao #move o jacaré junto com a tela
        self.speedy = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # Atualização da posição do jacaré
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.left < -largura_jacare:
            self.rect.x = random.randint(700+largura_jacare, 1400)
        
        
#------------------------Fim classe do jacaré------------------------------     

#----------------Classe da bala (munição)

class Bullet(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, img, bottom, centerx):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.speedx = 10  # Velocidade fixa para cima

    def update(self):
        # A bala só se move no eixo y
        self.rect.x += self.speedx

        # Se o tiro passar do inicio da tela, morre.
        if self.rect.centerx > 715:
            self.kill()


#------------------------Fim classe da bala------------------------------     

#==================================FIM DAS CLASSES==================================

clock = pygame.time.Clock()
FPS = 60

#==================================GRUPOS==================================

todos_objetos = pygame.sprite.Group()
grupo_jacare = pygame.sprite.Group()
grupo_balas = pygame.sprite.Group()
todos_desenhos = pygame.sprite.Group()

jogador = Fox(fox_imagem, todos_objetos, grupo_balas, bala_imagem, 300)
inimigo = Jacare(jacare_imagem)

grupo_jacare.add(inimigo)

todos_objetos.add(inimigo)
todos_objetos.add(jogador)

#==================================LOOP PRINCIPAL==================================
pygame.mixer.music.play(loops=-1) #inicia a música

while inicial:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inicial = False
            game = False #para sair do jogo
            final = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                inicial = False

    window.fill(cor_preto) 
    window.blit(fundo_inicial, (0, 0))
    inicial_texto1 = fonte2.render("Fox Supremacy", True, (150,0,0))
    posicao_inical_texto1 = inicial_texto1.get_rect()
    posicao_inical_texto1.center = (posicao_x, 150)
    inicial_texto2 = fonte3.render("Pressione ESPAÇO para jogar", True, cor_branco)
    posicao_inical_texto2 = inicial_texto2.get_rect()
    posicao_inical_texto2.center = (posicao_x, 380)
    posicao_instru = inicial_texto1.get_rect()
    posicao_instru.center = (520, 410)
    window.blit(inicial_texto1, posicao_inical_texto1)
    window.blit(inicial_texto2, posicao_inical_texto2)
    window.blit(instru, posicao_instru)

    pygame.display.update()


while game:
    
    clock.tick(FPS)

    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False #para sair do jogo
            final = False
        if event.type == pygame.KEYDOWN: #se uma tecla é apertada
            if jogador.rect.bottom >= 550:
                if event.key == pygame.K_UP: 
                    jogador.speedy=-4 #faz a raposa subir com 4 de velocidade
            if event.key == pygame.K_RIGHT: 
                jogador.speedy=0
            if event.key == pygame.K_SPACE: #apertando espaço, a raposa atira
                jogador.shoot()
                contador_balas+=1 
        
        
    # atualiza posição ( por enquanto zerada)
    todos_objetos.update()
    
    #--------------colisões--------------
    #JOGADOR COM JACARÉ:
    hits = pygame.sprite.spritecollide(jogador, grupo_jacare, True, pygame.sprite.collide_mask)
    
    #BALA COM JACARÉ:
    hits2 = pygame.sprite.groupcollide(grupo_balas, grupo_jacare, True, True, pygame.sprite.collide_mask)
    
    for hit in hits: 
        inimigo=Jacare(jacare_imagem)
        grupo_jacare.add(inimigo)
        todos_objetos.add(inimigo) #para o jacaré aparecer de novo
        vidas-=1
        if vidas == 0:
            game = False
        
    for hit in hits2:
        placar+=100
        contador_mais100+=1
        inimigo=Jacare(jacare_imagem)
        grupo_jacare.add(inimigo)
        todos_objetos.add(inimigo) #para o jacaré aparecer de novo

    #----------------Fundo infinito
    if x <= -700:
        x = 0
    else:
        x-=(3*aceleracao)

    if contador_mais100 > 2*FPS:
        contador_mais100 = 0
    if contador_mais100 > 0:
        contador_mais100+=1

    # ----------------Timer das balas
    if contador_balas >= 5*FPS: #transforma p segundos
        contador_balas = 0
    if contador_balas > 0:
        contador_balas+=1

    # ----------------Aumenta a aceleração
    if placar>1000:
        aceleracao = math.log(placar,10)-2

    # ----------------Gera saídas
    
    window.fill(cor_preto)  # Preenche com a cor branca
    window.blit(fundo_de_tela, (x, 0))
    window.blit(fundo_de_tela2, ((700+x), 0)) #anda o fundo da tela
    window.blit(jogador.image, jogador.rect)
    todos_objetos.draw(window)
    if contador_mais100 > 0:
        mais100 = fonte3.render("+100", True, (255,0,0))
        posicao_mais100 = mais100.get_rect()
        posicao_mais100.center = (650, 80)
        window.blit(mais100, posicao_mais100)
        
    if contador_balas == 0:
        window.blit(arma_imagem, ponto_arma)
    for i in range(0, vidas):
        window.blit(coracoes[i], pontos_coracoes[i])

    placar_texto = fonte.render("{:08d}".format(placar), True, cor_branco)
    posicao_placar = placar_texto.get_rect()
    posicao_placar.center = (575, 50)
    window.blit(placar_texto, posicao_placar)

    # ----------------Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

    if pausa_inicial:
        time.sleep(2)
        pausa_inicial = False

    # ----------------Aumenta o placar
    placar+=int(aceleracao//1)



while final:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            final = False
        if event.type == pygame.KEYDOWN:
            final = False
        

    window.fill(cor_preto) 
    window.blit(fundo_final, (0, 0))
    
    final_texto1 = fonte2.render("Fox Supremacy", True, cor_branco)
    finaliza(final_texto1, (posicao_x, 100))
    
    final_texto2 = fonte.render("Sua pontuação:", True, cor_branco)
    finaliza(final_texto2, (posicao_x, 470))
    
    final_texto3 = fonte.render("{} pontos".format(placar), True, cor_branco)
    finaliza(final_texto3, (posicao_x, 520))

    pygame.display.update()



pygame.quit()  # Função do PyGame que finaliza os recursos utilizados



#FIM DO CÓDIGO