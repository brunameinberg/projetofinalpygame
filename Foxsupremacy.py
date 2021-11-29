#-----importa bibliotecas
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
altura_bala = 20
largura_bala = 30 
altura_coracao = 20
largura_coracao = 30 
#----imagens
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
coracao_imagem = pygame.image.load('coracao.png').convert_alpha()
coracao_imagem = pygame.transform.scale(coracao_imagem, (largura_coracao, altura_coracao))



#-----para animação da raposa
fox_anim = []
for i in range(4):
    # Os arquivos de animação são numerados de 00 a 08
    filename = 'imagens/fox{}.png'.format(i+1)
    img = pygame.image.load(filename).convert_alpha()
    img = pygame.transform.scale(img, (75, 80))
    fox_anim.append(img)

#-----carrega o som

pygame.mixer.music.load('sons/mfundoof.wav') #musica de fundo
pygame.mixer.music.set_volume(0.4) #define o volume
bullet_sound=pygame.mixer.Sound('sons/bala.wav') #som da bala



#-----variaveis globais
x=0

# ----- Inicia estruturas de dados
# Definindo os novos tipo

#-----classe da raposa
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
        # A nova bala vai ser criada logo acima e no centro horizontal da nave
        nova_bala = Bullet(self.bala_imagem, self.rect.bottom-25 , self.rect.centerx+44)
        self.todos_objetos.add(nova_bala)
        self.grupo_balas.add(nova_bala)

#------------------------fim classe da raposa------------------------------

#-----classe do jacaré

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
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # Atualização da posição do jacaré
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.left < -largura_jacare:
            self.rect.x = random.randint(700+largura_jacare, 1400)
        
        
#------------------------fim classe do jacaré------------------------------     


#-----classe da bala 

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


#------------------------fim classe da bala------------------------------     


clock = pygame.time.Clock()
FPS = 60

#criando grupos----------

todos_objetos = pygame.sprite.Group()
grupo_jacare = pygame.sprite.Group()
grupo_balas = pygame.sprite.Group()

jogador = Fox(fox_imagem, todos_objetos, grupo_balas, bala_imagem, 300)
inimigo = Jacare(jacare_imagem)


grupo_jacare.add(inimigo)
todos_objetos.add(inimigo)
todos_objetos.add(jogador)




# ==================== Loop principal =====================
pygame.mixer.music.play(loops=-1) #inicia a música

while game:
    
    clock.tick(FPS)

    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False #para sair do jogo
        if event.type == pygame.KEYDOWN: #se uma tecla é apertada
            if jogador.rect.bottom >= 550:
                if event.key == pygame.K_UP: 
                    jogador.speedy=-4 #faz a raposa subir com 4 de velocidade
            if event.key == pygame.K_RIGHT: 
                jogador.speedy=0
            if event.key == pygame.K_SPACE: #apertando espaço, a raposa atira
                jogador.shoot() 
        
        
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
    ###########ESSA PARTE DE BAIXO TEM QUE AJUSTAR########
        if len(hits)>3: 
            game = False
###################################################################
        
    for hit in hits2:
        inimigo=Jacare(jacare_imagem)
        grupo_jacare.add(inimigo)
        todos_objetos.add(inimigo) #para o jacaré aparecer de novo

    

    # ------- Fundo infinito
    if x <= -700:
        x = 0
    else:
        x-=2
    
    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor branca
    window.blit(fundo_de_tela, (x, 0))
    window.blit(fundo_de_tela2, ((700+x), 0)) #anda o fundo da tela
    window.blit(jogador.image, jogador.rect)
    todos_objetos.draw(window)

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

 #para o fundo andar no sentido correto

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados



#placar
#aceleração
#vidas
#arumar o pulo
#limitar o numero de tiros