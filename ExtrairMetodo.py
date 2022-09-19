from Foxsupremacy import *
largura = 700
altura = 600
import pygame
window = pygame.display.set_mode((largura, altura)) #tamanho da tela


def finaliza (final_texto, posicao):
    posicao_final = final_texto.get_rect()
    posicao_final.center = posicao
    return window.blit(final_texto, posicao_final)