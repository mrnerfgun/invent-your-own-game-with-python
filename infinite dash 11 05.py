import pygame, sys, random
pygame.init()

WIDTH, HEIGHT=800, 400
screen=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless runner")
clock=pygame.time.Clock()
FPS=random.randint(60, 100)
WHITE=(255, 255, 255)
BLACK=(0, 0, 0)
BLUE=(50, 150, 255)
GREEN=(50, 255, 50)
RED=(255, 50, 50)
font = pygame.font.Font(None, 36)
player = pygame.Rect(100, HEIGHT - 140, 40, 60)
player_y_vel=0
gravity=0.8
jump_force=-15
on_ground=True

ground_height=80
ground_y=HEIGHT=ground_height

obstacle_width = 40
obstacle_height = 60
obstacle_speed = 6
obstacles = [pygame.Rect(WIDTH + 200, ground_y - obstacle_height, obstacle_width, obstacle_height)]
score=0
game_over=False
running=True

def reset_game():
    global player, player_y_vel, on_ground, game_over, obstacles, score
    player.x=100
    player.y=ground_y-player.height
    player_y_vel=0
    on_ground=True
    obstacles=[pygame.Rect(WIDTH + 200, ground_y - obstacle_height, obstacle_width, obstacle_height)]
    score=0
    game_over=False

while running:
    dt=clock.tick(FPS)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()   
    keys=pygame.key.get_pressed()
    if not game_over:
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and on_ground:
            player_y_vel=jump_force
            on_ground=False

        if keys[pygame.K_r] and on_ground:
            score=0 
            reset_game()
        
        player_y_vel+=gravity
        player.y+=player_y_vel
        if player.bottom>=ground_y:
            player.bottom=ground_y
            player_y_vel=0
            on_ground=True
        
        for obs in obstacles:
            obs.x-=obstacle_speed
            if obs.right<0:
                obstacles.remove(obs)
                obstacles.append(pygame.Rect(WIDTH + random.randint(200, 400), ground_y - obstacle_height, obstacle_width, obstacle_height))
                score+=1
        
        for obs in obstacles:
            if player.colliderect(obs):
                running=False
                print(f'Game over! Final score: {score}')

        screen.fill(WHITE)
        pygame.draw.rect(screen, GREEN, (0, ground_y, WIDTH, ground_height))
        pygame.draw.rect(screen, BLUE, player)
        for obs in obstacles:
            pygame.draw.rect(screen, RED, obs)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
