import random, sys, pygame
pygame.init()
WIDTH, HEIGHT=800, 600
screen=pygame.display.set_mode((WIDTH, HEIGHT))
clock=pygame.time.Clock()
BLUE=(0,150,255)
RED=(255,60,60)
WHITE=(255,255,255)
BLACK=(0,0,0)
GREEN=(0, 200, 0)
font=pygame.font.Font(None, 36)
player=pygame.Rect(WIDTH//2-20, HEIGHT-60, 40, 40)
player_speed=6
player_hp=5
player_bullets=[]
enemy_bullets=[]
bullet_speed=10
player_cooldown=200
enemy_cooldown=800
last_player_shot=0