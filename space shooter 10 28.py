import pygame,sys,random
pygame.init()
WIDTH,HEIGHT=800,600
screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock=pygame.time.Clock()
BLUE=(0,150,255)
RED=(255,60,60)
WHITE=(255,255,255)
BLACK=(0,0,0)   
player=pygame.Rect(WIDTH//2-20,HEIGHT-60,40,40)
player_speed=6
player_bullets=[]
enemy_bullets=[]
bullet_speed=10
player_cooldown=200
enemy_cooldown=800
last_player_shot=pygame.time.get_ticks()
running=True
player_hp=5
wave=1
enemies=[]
wave_active=False
enemy_speed=3
font=pygame.font.Font(None,36)
game_over=False
paused=False
FPS=60

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_p:
                paused = not paused

    keys=pygame.key.get_pressed()
    now=pygame.time.get_ticks()

    if keys[pygame.K_r]:
        player_hp=5
        wave=1
        enemies.clear()
        player_bullets.clear()
        enemy_bullets.clear()
        wave_active=False
        enemy_speed=3
        game_over=False
        print("Game restarted!")

    if game_over:
        screen.fill(BLACK)
        over_text=font.render("GAME OVER – Press R to Restart",True,RED)
        screen.blit(over_text,(WIDTH//2-200,HEIGHT//2))
        pygame.display.flip()
        clock.tick(60)
        continue

    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.left>0:
        player.x-=player_speed
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.right<WIDTH:
        player.x+=player_speed
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.top>0:
        player.y-=player_speed
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.bottom<HEIGHT:
        player.y+=player_speed   

    if keys[pygame.K_SPACE] and now-last_player_shot>player_cooldown:
        bullet=pygame.Rect(player.centerx-3,player.top-10,6,12)
        player_bullets.append(bullet)
        last_player_shot=now
    
    if keys[pygame.K_ESCAPE]:
        running=False
        pygame.QUIT
        sys.exit()

    if keys[pygame.K_p]:
        paused=not paused

    if paused:
        screen.fill(BLACK)
        pause_text = font.render("PAUSED - Press P to Resume", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - 180, HEIGHT // 2))
        pygame.display.flip()
        clock.tick(FPS)
        continue

    if not wave_active:
        enemies=[]
        for i in range(random.randint(2,3+wave)):
            e={"rect":pygame.Rect(random.randint(0,WIDTH-40),random.randint(20,150),40,40),
               "speed":random.choice([-1,1])*enemy_speed,
               "last_shot":now}
            enemies.append(e)
        wave_active=True
        print(f"Wave {wave} started with {len(enemies)} enemies!")
    for e in enemies:
        rect=e["rect"]
        step=int(e["speed"]) if abs(e["speed"])>=1 else (1 if e["speed"]>0 else -1)
        rect.x+=step
        if rect.left<0:
            rect.left=0
            e["speed"]*=-1
            rect.x+=int(e["speed"])  
        if rect.right>WIDTH:
            rect.right=WIDTH
            e["speed"]*=-1
            rect.x+=int(e["speed"])
        if now-e["last_shot"]>enemy_cooldown:
            e_bullet=pygame.Rect(rect.centerx-3,rect.bottom+6,6,12)
            enemy_bullets.append(e_bullet)
            e["last_shot"]=now


    for b in player_bullets:
        b.y-=bullet_speed
    for b in enemy_bullets:
        b.y+=bullet_speed

    player_bullets=[b for b in player_bullets if b.bottom>0]
    enemy_bullets=[b for b in enemy_bullets if b.top<HEIGHT]

    for b in player_bullets[:]:
        hit=None
        for e in enemies:
            if b.colliderect(e["rect"]):
                hit=e
                break
        if hit:
            player_bullets.remove(b)
            enemies.remove(hit)
            print("Enemy destroyed!")

    for e_b in enemy_bullets[:]:
        if e_b.colliderect(player):
            enemy_bullets.remove(e_b)
            player_hp-=1
            print(f"Player hit! {player_hp} HP left.")
            player.x=WIDTH//2-20
            player.y=HEIGHT-60
            if player_hp<=0:
                game_over=True

    if len(enemies)==0:
        wave_active=False
        wave+=1
        enemy_speed+=0.5
        enemy_cooldown=max(300,int(enemy_cooldown*0.95))
        print(f"Wave {wave-1} cleared! Next wave: {wave}")

    screen.fill(BLACK)
    pygame.draw.rect(screen,BLUE,player)
    for e in enemies:
        pygame.draw.rect(screen,RED,e["rect"])
    for b in player_bullets:
        pygame.draw.rect(screen,BLUE,b)
    for b in enemy_bullets:
        pygame.draw.rect(screen,RED,b)
    hp_text=font.render(f"HP: {player_hp}",True,WHITE)
    wave_text=font.render(f"Wave: {wave}",True,WHITE)
    screen.blit(hp_text,(10,10))
    screen.blit(wave_text,(10,40))
    pygame.display.flip()
    clock.tick(60)
