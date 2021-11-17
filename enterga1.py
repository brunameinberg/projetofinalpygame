import pygame

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
fundo_de_tela = pygame.image.load('imagens/fundo.png').convert_alpha()
fundo_de_tela = pygame.transform.scale(fundo_de_tela, (largura, altura))
fox_imagem = pygame.image.load('imagens/fox1.png').convert_alpha()
fox_imagem = pygame.transform.scale(fox_imagem, (largura_fox, altura_fox))
jacare_imagem = pygame.image.load('imagens/jacare.png').convert_alpha()
jacare_imagem = pygame.transform.scale(jacare_imagem, (largura_jacare, altura_jacare))


# ----- Inicia estruturas de dados
# Definindo os novos tipo
class Fox(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = 130
        self.rect.bottom = 550
        self.speedx = 0
        self.speedy = 0

    def update(self):
        # Atualização da posição da raposa
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Mantem dentro da tela
        if self.rect.right > largura:
            self.rect.right = largura
        if self.rect.left < 0:
            self.rect.left = 0

class Jacare(pygame.sprite.Sprite):
    def __init__(self, img):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.centerx = 500
        self.rect.bottom = 550
        self.speedx = 0
        self.speedy = 0

    def update(self):
        # Atualização da posição do jacaré
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Mantem dentro da tela
        if self.rect.right > largura:
            self.rect.right = largura
        if self.rect.left < 0:
            self.rect.left = 0

clock = pygame.time.Clock()
FPS = 60

jogador = Fox(fox_imagem)
inimigo = Jacare(jacare_imagem)

x=0
# ===== Loop principal =====
while game:

    clock.tick(FPS)


    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False

    # atualiza posição ( por enquanto zerada)7
    jogador.update()
    inimigo.update()

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor branca
    window.blit(fundo_de_tela, (x, 0))
    window.blit(fundo_de_tela, (700-x, 0))
    window.blit(jogador.image, jogador.rect)
    window.blit(inimigo.image, inimigo.rect)


    

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

    x-=10

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados

