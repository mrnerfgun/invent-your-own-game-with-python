import pygame, sys, random, math, time
from pygame.locals import *
pygame.init()
font = pygame.font.SysFont(None, 24)
TILE=24
ROWS=21
COLS=21
WIDTH=COLS*TILE
HEIGHT=ROWS*TILE
player_lives=3
FPS=60
screen=pygame.display.set_mode((WIDTH, HEIGHT))
clock=pygame.time.Clock()
score=0
BLACK=(0, 0, 0)
BLUE=(0, 0, 180)
YELLOW=(255, 255, 0)
WHITE=(255, 255, 255)
RED=(255, 50, 50)
game_over=False
paused=False
frightened_timer=0
ghost_frightened=False
fruit_score=100
maze=[
    "WWWWWWWWWWWWWWWWWWWWWW",
    "WG:.......S........:GW",
    "W.WWWW.WW.WW.WWWW.WW.W",
    "W.WWWW.WW.WW.WWWW.WW.W",
    "W....................W",
    "W.WW.WWWWWWWWW.WW.WW.W",
    "W....W...W...W....W..W",
    "WWWW.WWW W WWW.WWWWWWW",
    "W.........;..........W",
    "WWWW.WW W W WW.WWWWWWW",
    "W:........P.........:W",
    "WWWW.WW WWWWW WW.WWWWW",
    "W.....W.........W....W",
    "WWWW.WWW W WWW.WWWWW.W",
    "W....W...W...W....W..W",
    "W.WW.WWWWWWWWW.WW.WW.W",
    "W.........;..........W",
    "W.WWWW.WW.WW.WWWW.WW.W",
    "W.WWWW.WW.WW.WWWW.WW.W",
    "WG:.......W........:GW",
    "WWWWWWWWWWWWWWWWWWWWWW",
]

pellets=[]
walls=[]
player_x=player_y=0
ghosts=[]
b_pellets=[]
fruit=[]
super_fruits=[]
class ghost:
    def __init__(self, x, y, color):
        self.rect=pygame.Rect(x - 12, y - 12, 24, 24)
        self.color=color
        self.speed=2
        self.direction=pygame.Vector2(1, 0)
    
    def draw(self, screen, frightened=False):
        color=(0, 0, 255) if frightened else self.color
        pygame.draw.circle(screen, color, self.rect.center, 12)
        
    
    def move(self, walls, player_rect):
        new_rect = self.rect.move(int(self.direction.x * self.speed), int(self.direction.y * self.speed))
        if any(new_rect.colliderect(w) for w in walls):
            self.choose_new_direction(walls, player_rect)
            return
        
        self.rect=new_rect

        if self.rect.centerx%TILE==0 and self.rect.centery%TILE==0:
            self.choose_new_direction(walls, player_rect)
    
    def choose_new_direction(self, walls, player_rect):
        possible_dirs = [
        pygame.Vector2(1, 0),
        pygame.Vector2(-1, 0),
        pygame.Vector2(0, 1),
        pygame.Vector2(0, -1)
        ]
        valid_dirs=[]
        for d in possible_dirs:
            test=self.rect.move(int(d.x*self.speed), int(d.y*self.speed))
            if not any(test.colliderect(w) for w in walls):
                valid_dirs.append(d)

        if len(valid_dirs)>1:
            opposite=pygame.Vector2(-self.direction.x, -self.direction.y)
            if opposite in valid_dirs:
                valid_dirs.remove(opposite)

        target=pygame.Vector2(player_rect.center)
        best_dir=None
        best_dist=float("inf")

        for d in valid_dirs:
            next_pos=pygame.Vector2(self.rect.center)+d*(TILE*5)
            dist=(next_pos-target).length_squared()
            if dist<best_dist:
                best_dist=dist
                best_dir=d

        if ghost_frightened:
            best_dir=random.choice(valid_dirs)

        
        if best_dir:
            self.direction=best_dir
        elif valid_dirs:
            self.direction = random.choice(valid_dirs)

        else:
            self.direction=random.choice(valid_dirs)

for r, row in enumerate(maze):
    for c, char in enumerate(row):
        if char=="W":
            walls.append(pygame.Rect(c * TILE, r * TILE, TILE, TILE))
        elif char==".":
            pellets.append(pygame.Rect(c*TILE+TILE//2, r*TILE+TILE//2, 4, 4))
        elif char=="P":
            player_x=c*TILE+TILE//2
            player_y=r*TILE+TILE//2
        elif char=="G":
            ghosts.append(ghost(c*TILE+TILE//2, r*TILE+TILE//2, (255, 0, 0)))
        elif char==":":
            b_pellets.append(pygame.Rect(c*TILE+TILE//2, r*TILE+TILE//2, 12, 12))
        elif char==";":
            fruit.append(pygame.Rect(c*TILE+TILE//2, r*TILE+TILE//2, 12, 12))
        elif char=="S":
            super_fruits.append(pygame.Rect(c*TILE+TILE//2, r*TILE+TILE//2, 12, 12))

            

player_rect=pygame.Rect(player_x-12, player_y-12, 24, 24)
speed=2
direction=pygame.Vector2(0, 0)
desired_direction=pygame.Vector2(0, 0)
score=0
running=True

def can_move(dir):
    test=player_rect.move(int(dir.x*speed), int(dir.y*speed))
    return not any(test.colliderect(w) for w in walls)

def reset_game():
    global score, direction, desired_direction, player_rect, pellets, ghosts, player_lives, frightened_timer, ghost_frightened, b_pellets, super_fruits
    super_fruits=[]
    b_pellets=[]
    player_lives=3
    score=0
    direction=pygame.Vector2(0, 0)
    desired_direction=pygame.Vector2(0, 0)
    player_rect=pygame.Rect(player_x-12, player_y-12, 24, 24)
    pellets=[]
    ghosts=[]
    for r, row in enumerate(maze):
        for c, char in enumerate(row):
            if char==".":
                pellets.append(pygame.Rect(c*TILE+TILE//2, r*TILE+TILE//2, 4, 4))
            elif char==":":
                b_pellets.append(pygame.Rect(c*TILE+TILE//2, r*TILE+TILE//2, 12, 12))
            elif char==";":
                fruit.append(pygame.Rect(c*TILE+TILE//2, r*TILE+TILE//2, 12, 12))
            elif char=="S":
                super_fruits.append(pygame.Rect(c*TILE+TILE//2, r*TILE+TILE//2, 12, 12))
    
    for p in pellets[:]:
        if player_rect.collidepoint(p.center):
            pellets.remove(p)
    
    for r, row in enumerate(maze):
        for c, char in enumerate(row):
            if char=="G":
                ghosts.append(ghost(c*TILE+TILE//2, r*TILE+TILE//2, (255, 0, 0)))
    

def draw_pacman(screen, rect, direction, mouth_open):
    cx, cy=rect.center
    radius=12
    if direction.length_squared()==0:
        angle=0  
    else:
        angle=direction.angle_to(pygame.Vector2(1, 0))
    mouth=40 if mouth_open else 0

    start_angle=math.radians(mouth) + math.radians(angle)
    end_angle=math.radians(360 - mouth) + math.radians(angle)

    pygame.draw.circle(screen, YELLOW, (cx, cy), radius)
    pygame.draw.polygon(screen, BLACK, [
        (cx, cy),
        (cx + radius * math.cos(start_angle), cy - radius * math.sin(start_angle)),
        (cx + radius * math.cos(end_angle),   cy - radius * math.sin(end_angle)),
    ])


def terminate():
    pygame.quit()
    sys.exit()

while running:
    clock.tick(FPS)
    screen.fill(BLACK)
    ghost_frightened=pygame.time.get_ticks()<frightened_timer
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_r:
                reset_game()
                game_over=False
            if event.key==pygame.K_ESCAPE:
                running=False
                terminate()
            if event.key==pygame.K_p:
                paused=not paused
    
    keys=pygame.key.get_pressed()
    if not game_over and not paused:
        if (keys[pygame.K_UP] or keys[pygame.K_w]):
            desired_direction=pygame.Vector2(0, -1)
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            desired_direction=pygame.Vector2(0, 1)
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            desired_direction=pygame.Vector2(-1, 0)
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            desired_direction=pygame.Vector2(1, 0)
        if can_move(desired_direction):
            direction=desired_direction

        if can_move(direction):
            player_rect.x+=int(direction.x*speed)
            player_rect.y+=int(direction.y*speed)
            
        for wall in walls:
            pygame.draw.rect(screen, BLUE, wall)
        
        for p in pellets[:]:
            if player_rect.collidepoint(p.center):
                pellets.remove(p)
                score+=1
            else:
                pygame.draw.circle(screen, YELLOW, p.center, 4)
        
        for bp in b_pellets[:]:
            if player_rect.collidepoint(bp.center):
                b_pellets.remove(bp)
                score+=5
                frightened_timer=pygame.time.get_ticks()+6000
        for f in fruit:
            if player_rect.collidepoint(f.center):
                fruit.remove(f)
                score+=fruit_score

    if paused:
        screen.fill(BLACK)
        pause_text = font.render("PAUSED - Press P to Resume", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - 180, HEIGHT // 2))
        pygame.display.flip()
        clock.tick(FPS)
        continue
    for bp in b_pellets:
        pygame.draw.circle(screen, WHITE, bp.center, 8)

    for f in fruit:
        pygame.draw.circle(screen, RED, f.center, 8)

    for s in super_fruits:
        pygame.draw.circle(screen, BLUE, s.center, 8)

    for g in ghosts[:]:
        g.move(walls, player_rect)
        g.draw(screen, ghost_frightened)
        if player_rect.colliderect(g.rect):
            if player_rect.colliderect(g.rect):
                if ghost_frightened:
                    score += 50
                    ghosts.remove(g)   
                    continue
            if player_lives > 1 and not ghost_frightened:
                player_lives -= 1
                player_rect.x = player_x - 12
                player_rect.y = player_y - 12
                direction = pygame.Vector2(0,0)
                desired_direction = pygame.Vector2(0,0)
                ghosts.clear()
                for r, row in enumerate(maze):
                    for c, char in enumerate(row):
                        if char=="G":
                            ghosts.append(ghost(c*TILE+TILE//2, r*TILE+TILE//2, (255, 0, 0)))
            else:
                player_lives = 0
                game_over = True
            

            break



    if player_lives<=0:
        game_over=True
        text=font.render(f"You lose. Press r to restart. Final score: {score}", True, WHITE)
        screen.blit(text, (100, 100))


    if not pellets:
        game_over=False
        text=font.render("You won!", True, WHITE)
        screen.blit(text, (100, 100))
        pygame.display.flip()
        time.sleep(5)
        score+=100
        for r, row in enumerate(maze):
            for c, char in enumerate(row):
                if char=="W":
                    walls.append(pygame.Rect(c * TILE, r * TILE, TILE, TILE))
                elif char==".":
                    pellets.append(pygame.Rect(c*TILE+TILE//2, r*TILE+TILE//2, 4, 4))
                elif char=="P":
                    player_x=c*TILE+TILE//2
                    player_y=r*TILE+TILE//2
                elif char=="G":
                    ghosts.append(ghost(c*TILE+TILE//2, r*TILE+TILE//2, (255, 0, 0)))
                elif char==":":
                    b_pellets.append(pygame.Rect(c*TILE+TILE//2, r*TILE+TILE//2, 12, 12))
                elif char==";":
                    fruit.append(pygame.Rect(c*TILE+TILE//2, r*TILE+TILE//2, 12, 12))
                elif char=="S":
                    super_fruits.append(pygame.Rect(c*TILE+TILE//2, r*TILE+TILE//2, 12, 12))
        direction=pygame.Vector2(0, 0)
        desired_direction=pygame.Vector2(0, 0)
        player_rect=pygame.Rect(player_x-12, player_y-12, 24, 24)
        fruit_score+=100
        continue

    if score>=10000:
        score=0
        player_lives+=1
    
    
    if not ghosts:
        for r, row in enumerate(maze):
            for c, char in enumerate(row):
                if char=="G":
                    ghosts.append(ghost(c*TILE+TILE//2, r*TILE+TILE//2, (255, 0, 0)))
                elif char==":":
                    b_pellets.append(pygame.Rect(c*TILE+TILE//2, r*TILE+TILE//2, 12, 12))
                elif char==";":
                    fruit.append(pygame.Rect(c*TILE+TILE//2, r*TILE+TILE//2, 12, 12))



    mouth_open=pygame.time.get_ticks() // 150 % 2 == 0  
    draw_pacman(screen, player_rect, direction, mouth_open)
    font=pygame.font.SysFont(None, 24)
    text=font.render(f"score: {score}", True, WHITE)
    text2=font.render(f"lives: {player_lives}", True, WHITE)
    screen.blit(text, (10, 5))
    screen.blit(text2, (10, 30))
    pygame.display.update()