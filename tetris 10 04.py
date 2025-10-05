#Tetris
import pygame, sys, random
from pygame.locals import *
ROWS=20
COLS=10
BLOCK_SIZE=30
WIDTH=COLS*BLOCK_SIZE
HEIGHT=ROWS*BLOCK_SIZE
FPS=60
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE=(255, 255, 255)
COLORS = {
    'I': (0, 255, 255),     
    'O': (255, 255, 0),     
    'T': (128, 0, 128),     
    'S': (0, 255, 0),       
    'Z': (255, 0, 0),       
    'J': (0, 0, 255),       
    'L': (255, 165, 0),     
}

SHAPES = {
    'I': [
        [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        [
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 0]
        ]
    ],
    'O': [
        [
            [1, 1],
            [1, 1]
        ]
    ],
    'T': [
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]
        ],
        [
            [0, 1, 0],
            [0, 1, 1],
            [0, 1, 0]
        ],
        [
            [0, 0, 0],
            [1, 1, 1],
            [0, 1, 0]
        ],
        [
            [0, 1, 0],
            [1, 1, 0],
            [0, 1, 0]
        ]
    ],
    'S': [
        [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0]
        ],
        [
            [0, 1, 0],
            [0, 1, 1],
            [0, 0, 1]
        ]
    ],
    'Z': [
        [
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]
        ],
        [
            [0, 0, 1],
            [0, 1, 1],
            [0, 1, 0]
        ]
    ],
    'J': [
        [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ],
        [
            [0, 1, 1],
            [0, 1, 0],
            [0, 1, 0]
        ],
        [
            [0, 0, 0],
            [1, 1, 1],
            [0, 0, 1]
        ],
        [
            [0, 1, 0],
            [0, 1, 0],
            [1, 1, 0]
        ]
    ],
    'L': [
        [
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0]
        ],
        [
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 1]
        ],
        [
            [0, 0, 0],
            [1, 1, 1],
            [1, 0, 0]
        ],
        [
            [1, 1, 0],
            [0, 1, 0],
            [0, 1, 0]
        ]
    ]
}

class Tetromino:
    def __init__(self, name, x, y):
        self.name=name
        self.x=x
        self.y=y
        self.rotations=SHAPES[name]
        self.rotation_index=0
        self.color=COLORS[name]
    def rotate(self):
        self.rotation_index=(self.rotation_index + 1) % len(self.rotations)
        
    def move(self, dx, dy):
        self.x+=dx
        self.y+=dy

    @property
    def shape(self):
        return self.rotations[self.rotation_index]
    
    def draw(self, surface):
        shape=self.shape
        for row_index, row in enumerate(shape):
            for col_index, cell in enumerate(row):
                if cell==1:
                    x_pos=(self.x+col_index)*BLOCK_SIZE
                    y_pos=(self.y+row_index)*BLOCK_SIZE
                    pygame.draw.rect(surface, self.color, (x_pos, y_pos, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(surface, BLACK, (x_pos, y_pos, BLOCK_SIZE, BLOCK_SIZE), 1)


class Board:
    def __init__(self):
        self.grid=[[0 for i in range(COLS)] for i in range(ROWS)]
    
    def valid_position(self, tetromino):
        shape = tetromino.shape
        for row_idx, row in enumerate(tetromino.shape):
            for col_idx, cell in enumerate(row):
                if cell==0:
                    continue
                x=tetromino.x+col_idx
                y=tetromino.y+row_idx
                
                if x<0 or x>=COLS or y>=ROWS:
                    return False
                if y >= 0 and self.grid[y][x] != 0:
                    return False
        return True
    
    def place(self, tetromino):
        for row_idx, row in enumerate(tetromino.shape):
            for col_idx, cell in enumerate(row):
                if cell:
                    x=tetromino.x+col_idx
                    y=tetromino.y+row_idx
                    if 0<=x<COLS and 0<=y<ROWS:
                        self.grid[y][x]=tetromino.color

    def clear_full_rows(self):
        new_grid = []
        lines_cleared = 0

        for row in self.grid:
            if 0 not in row:
                lines_cleared += 1
            else:
                new_grid.append(row)

        for i in range(lines_cleared):
            new_grid.insert(0, [0 for _ in range(COLS)])

        self.grid = new_grid
        return lines_cleared
    
    def draw(self, surface):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell != 0:
                    pygame.draw.rect(
                        surface,
                        cell,
                        (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    )
                    pygame.draw.rect(
                        surface,
                        BLACK,
                        (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                        1
                )


class Game:
    def __init__(self):
        self.started=False
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock=pygame.time.Clock()
        self.board=Board()
        self.current_piece=self.get_new_piece()
        self.drop_timer=pygame.time.get_ticks()
        self.drop_speed=500
        self.running=True
        self.paused=False
        self.score=0
        self.font=pygame.font.SysFont("Arial", 24)

    def get_new_piece(self):
        name=random.choice(list(SHAPES.keys()))
        x=COLS//2-len(SHAPES[name][0][0])//2
        y=0
        return Tetromino(name, x, y)
    
    def reset(self):
        self.board=Board()
        self.current_piece=self.get_new_piece()
        self.running=True
        self.paused=False
        self.score=0
        self.started=True
    
    def run(self):
        while True:
            self.handle_events()
            if self.started and self.running and not self.paused:
                self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.running=False
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                if not self.started:
                    if not self.started and event.key==pygame.K_RETURN:
                        self.started=True
                        self.running=True

                if event.key in (pygame.K_LEFT, pygame.K_a):
                    self.current_piece.move(-1, 0)
                    if not self.board.valid_position(self.current_piece):
                        self.current_piece.move(1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.current_piece.move(1, 0)
                    if not self.board.valid_position(self.current_piece):
                        self.current_piece.move(-1, 0)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.current_piece.move(0, 1)
                    if not self.board.valid_position(self.current_piece):
                        self.current_piece.move(0, -1)
                elif event.key==pygame.K_SPACE:
                    while self.board.valid_position(self.current_piece):
                        self.current_piece.move(0, 1)
                    self.current_piece.move(0, -1)
                    self.board.place(self.current_piece)
                    lines = self.board.clear_full_rows()
                    self.score += lines * 100
                    self.current_piece = self.get_new_piece()
                    self.drop_timer=pygame.time.get_ticks()
                    if not self.board.valid_position(self.current_piece):
                        self.running = False
                elif event.key in (pygame.K_UP, pygame.K_f):
                    old_index = self.current_piece.rotation_index
                    self.current_piece.rotate()
                    if not self.board.valid_position(self.current_piece):
                        self.current_piece.rotation_index = old_index

                if event.key==pygame.K_p:
                    self.paused=not self.paused
                if event.key==pygame.K_r:
                    self.reset()
                if event.key==pygame.K_ESCAPE:
                    sys.exit()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.drop_timer > self.drop_speed:
            self.drop_timer = current_time  # reset timer
            self.current_piece.move(0, 1)
        if not self.board.valid_position(self.current_piece):
            self.current_piece.move(0, -1)
            self.board.place(self.current_piece)
            lines = self.board.clear_full_rows()
            self.score += lines * 100
            self.current_piece = self.get_new_piece()
            if not self.board.valid_position(self.current_piece):
                self.running = False

    def draw_text(self, text, size, color, x, y):  
        font = pygame.font.SysFont("Arial", size)
        label = font.render(text, True, color)
        self.screen.blit(label, (x, y))
    
    def draw(self):
        self.screen.fill(BLACK)
        if not self.started:
            self.draw_text("TETRIS", 64, WHITE, WIDTH // 2 - 100, HEIGHT // 2 - 100)
            self.draw_text("Press ENTER to Start", 32, WHITE, WIDTH // 2 - 140, HEIGHT // 2)
            pygame.display.flip()
            return
        self.board.draw(self.screen)
        self.current_piece.draw(self.screen)
        self.draw_text(f"Score: {self.score}", 24, WHITE, 10, 10)  
        if self.paused:
            self.draw_text("Paused", 48, WHITE, WIDTH // 2 - 80, HEIGHT // 2 - 30)  
        elif not self.running:
            self.draw_text("Game Over", 48, WHITE, WIDTH // 2 - 120, HEIGHT // 2 - 30)  
            self.draw_text("Press R to Restart", 24, WHITE, WIDTH // 2 - 100, HEIGHT // 2 + 20)  

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()
