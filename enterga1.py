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

altura_fox = 75
largura_fox = 80
fundo_de_tela = pygame.image.load('imagens/fundo.png').convert() #carrega imagem do fundo
fundo_de_tela = pygame.transform.scale(fundo_de_tela, (largura, altura)) #tamanho do fundo
fox_imagem = pygame.image.load('imagens/fox1.png').convert() #carrega imagem da raposa
fox_imagem = pygame.transform.scale(fox_imagem, (largura_fox, altura_fox)) #tamanho da raposa



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
        # Atualização da posição da nave
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Mantem dentro da tela
        if self.rect.right > largura:
            self.rect.right = largura
        if self.rect.left < 0:
            self.rect.left = 0

clock = pygame.time.Clock()
FPS = 30

jogador = Fox(fox_imagem)

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

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor branca
    window.blit(fundo_de_tela, (0, 0))
    window.blit(jogador.image, jogador.rect)

    

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados

