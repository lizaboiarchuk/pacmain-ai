import pygame
import sys
import random
from settings import *
from player_class import *

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = WIDTH//28
        self.cell_height = HEIGHT//30
        self.walls = []
        self.coins = []
        self.free = []
        self.p_pos = None
        self.load()
        self.player = Player(self, self.p_pos)


    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                self.running == False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()


######################### helper functions ######################
    def draw_text(self, words, screen, pos, size, color, font_name):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        pos[0] = pos[0]-text_size[0]//2
        pos[1] = pos[1]-text_size[1]//2
        screen.blit(text, pos)


    def load(self):
        self.background = pygame.image.load('pacmanSprites/background.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.candy = pygame.image.load('pacmanSprites/candy.png')
        self.candy = pygame.transform.scale(self.candy, (self.cell_width+10 ,self.cell_height+10))

        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vec(xidx, yidx))
                    elif char == "0":
                        self.free.append(vec(xidx, yidx))

        temp = random.choice(self.free)
        self.p_pos = [temp.x, temp.y]
        self.free.remove(self.p_pos)
        temp = random.choice(self.free)
        self.coins.append([temp.x,temp.y])


    def draw_grid(self):
        for x in range(WIDTH//self.cell_width):
            pygame.draw.line(self.screen, GREY, (x*self.cell_width, 0), (x*self.cell_width, HEIGHT))
        for x in range(HEIGHT//self.cell_height):
            pygame.draw.line(self.screen, GREY, (0, x*self.cell_height), (WIDTH, x*self.cell_height))


    def reset(self):
        self.player.direction *= 0
        self.coins = []
        self.walls = []
        self.free = []
        with open("walls.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == '1':
                        self.walls.append(vec(xidx, yidx))
                    elif char == "0":
                        self.free.append(vec(xidx, yidx))

        #self.p_pos = random.choice(self.free)
        temp = random.choice(self.free)
        self.p_pos = [temp.x, temp.y]
        temp = random.choice(self.free)
        self.coins.append([temp.x,temp.y])
        self.player = Player(self, self.p_pos)
        self.free.remove(self.p_pos)
        #self.coins.append(random.choice(self.free))
        self.state = "playing"



######################### intro functions ######################
    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'


    def start_update(self):
        pass


    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACE BAR', self.screen, [WIDTH//2, HEIGHT//2], START_TEXT_SIZE, (170, 132, 58), START_FONT)
        pygame.display.update()


######################### playing functions ######################
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


    def playing_update(self):
        self.player.update()


    def playing_draw(self):
        self.screen.blit(self.background, (0,0))
        self.draw_coins()
        self.player.draw()
        pygame.display.update()


    def draw_coins(self):
        for coin in self.coins:
            self.screen.blit(self.candy, (int(coin[0]*self.cell_width-self.cell_width//2 + 6), int(coin[1]*self.cell_height-self.cell_height//2 + 5)))


########################### game over functions ################################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False


    def game_over_update(self):
        pass


    def game_over_draw(self):
        self.screen.fill(BLACK)
        quit_text = "Press the escape button to QUIT"
        again_text = "Press SPACE bar to PLAY AGAIN"
        self.draw_text("GAME OVER", self.screen, [WIDTH//2, 100],  25, RED, START_FONT)
        self.draw_text(again_text, self.screen, [
                       WIDTH//2, HEIGHT//2],  20, (190, 190, 190), START_FONT)
        self.draw_text(quit_text, self.screen, [
                       WIDTH//2, HEIGHT//1.5],  20, (190, 190, 190), START_FONT)
        pygame.display.update()
