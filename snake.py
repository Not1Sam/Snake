import pygame as pg
import os
import sys
import random
import json
import gc
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pg.init()
pg.display.set_caption("Snake")
pg.font.init()

#*Screen dimensions
width, height = 1280, 720
SCREEN = pg.display.set_mode((width, height))

#*Resource paths
back_loc = (r"snake_background.png")
apple_loc = (r"apple.png")
snake_head_loc = (r"snake_head.png")
snake_mouth_open_loc = (r"snake_mouth_open.png")
HighScore_loc = (r"HighScore.json")

#*Colors
background_color = '#F4FEEA'
body_color = '#3CCF4E'
text_color = '#1B4332'
btn = '#55A630'
btn_hover = '#74C947'
grid = '#95D5B2'
light_color = '#E9F5E1'
dark_color = '#D8EFC8'

#*Clock
clock = pg.time.Clock()

#*Font
title_font = pg.font.SysFont('pacifico regular', 70)
lm_font = pg.font.SysFont('pacifico regular', 60)
text_font = pg.font.SysFont('RobotoCondensed Black',30)

def main_menu():
    pg.display.set_caption("Main Menu")
    while True:
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        SCREEN.fill('white')
        background = pg.image.load(back_loc)
        SCREEN.blit(background, (0, 0))

        pg.draw.rect(SCREEN, text_color, (490, 100, 320, 10), border_radius=50)
        title = title_font.render('SNAKE:', True, text_color)
        SCREEN.blit(title, (495, 5))

        play_button = pg.Rect(488, 266, 324, 100)
        pg.draw.rect(SCREEN, text_color, play_button, border_radius=20)
        play_text = title_font.render('PLAY', True, btn)
        SCREEN.blit(play_text, (540, 250))

        leave_button = pg.Rect(488, 430, 324, 100)
        pg.draw.rect(SCREEN, text_color, leave_button, border_radius=20)
        leave_text = title_font.render('LEAVE', True, btn)
        SCREEN.blit(leave_text, (509, 420))

        if play_button.collidepoint(mouse):
            pg.draw.rect(SCREEN, btn_hover, play_button, border_radius=20)
            SCREEN.blit(play_text, (540, 250))
            if pg.mouse.get_pressed()[0]:
                gc.collect()
                game()

        if leave_button.collidepoint(mouse):
            pg.draw.rect(SCREEN, btn_hover, leave_button, border_radius=20)
            SCREEN.blit(leave_text, (509, 420))
            if pg.mouse.get_pressed()[0]:
                gc.collect()
                pg.quit()
                sys.exit()

        pg.display.update()
        
class HighScoreManager:
    def __init__(self, filename=HighScore_loc):
        self.filename = filename
        self.highscore = 0
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.highscore = data.get("highscore", 0)
            except (json.JSONDecodeError, IOError):
                self.highscore = 0
        else:
            self.highscore = 0

    def save(self, score):
        if score > self.highscore:
            self.highscore = score
            try:
                with open(self.filename, 'w') as f:
                    json.dump({"highscore": self.highscore}, f)
            except IOError:
                pass
                print(IOError) 

    def get(self):
        return self.highscore
                    
def game():
    pg.display.set_caption("Game")
    #*Assets
    apple = pg.image.load(apple_loc)
    apple = pg.transform.scale(apple, (40,40))
    #* Variables
    posx, posy = 80, 40
    score = 0
    direction = "right"
    tile_size = 40
    apple_x, apple_y = random.randint(0,31)*40, random.randint(1,17)*40
    snake_body = [(posx, posy), (posx-40, posy), (posx-80, posy)]
    highScore_manager = HighScoreManager()
    hsb = False

    running = True
    while running:
        SCREEN.fill(light_color)
        pg.draw.rect(SCREEN, text_color, (0,37,1280,3))
        for row in range(1, height // tile_size):
            for col in range(0, width // tile_size):
                color = light_color if (row + col) % 2 == 0 else dark_color
                pg.draw.rect(SCREEN, color, (col * tile_size, row * tile_size, tile_size, tile_size))

        score_txt = text_font.render("Score:", True, text_color)
        score_val = text_font.render(str(score), True, text_color)
        SCREEN.blit(score_txt, (30,4))
        SCREEN.blit(score_val, (115,4))

        HighScore = highScore_manager.get()
        highscore_txt = text_font.render("HighScore:", True, text_color)
        highscore_val = text_font.render(str(HighScore), True, text_color)
        SCREEN.blit(highscore_txt, (1000,4))
        SCREEN.blit(highscore_val, (1150,4))

        if score > HighScore:
            HighScore = score
            highScore_manager.save(HighScore)
            pg.display.set_caption("You Broke The HighScore !!!!!")
            hsb = True

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                gc.collect()
                pg.quit()
                sys.exit()
            elif ev.type == pg.KEYDOWN:
                if ev.key in (pg.K_w, pg.K_UP) and direction != "down":
                    direction = "up"
                elif ev.key in (pg.K_s, pg.K_DOWN) and direction != "up":
                    direction = "down"
                elif ev.key in (pg.K_a, pg.K_LEFT) and direction != "right":
                    direction = "left"
                elif ev.key in (pg.K_d, pg.K_RIGHT) and direction != "left":
                    direction = "right"

        head_x, head_y = snake_body[0]
        if direction == "up":
            head_y -= tile_size
        elif direction == "down":
            head_y += tile_size
        elif direction == "left":
            head_x -= tile_size
        elif direction == "right":
            head_x += tile_size

        new_head = (head_x, head_y)

        #* wall collision
        if not ( 0 <= head_x<=1240 and 40<= head_y<=680 ):
            break

        #* self collision 
        if new_head in snake_body:
            break

        snake_body = [new_head] + snake_body[:-1]

        #* apple collision
        if new_head == (apple_x, apple_y):
            score += 1
            apple_x, apple_y = random.randint(0,31)*40, random.randint(1,17)*40
            snake_body.append(snake_body[-1])

        for i, segment in enumerate(snake_body):
            color = "yellow" if i == 0 else ("red" if i == len(snake_body)-1 else body_color)
            pg.draw.rect(SCREEN, color, (segment[0], segment[1], 40, 40), border_radius=10)

        SCREEN.blit(apple, (apple_x, apple_y))
        pg.display.update()
        clock.tick(5)

    pg.image.save(SCREEN, "Finale.png")
    gc.collect()
    end_menu(hsb)
    
    
def end_menu(HSB):
    pg.time.delay(300)
    while True:
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gc.collect()
                pg.quit()
                sys.exit()
                
        pg.image.save(SCREEN,"Finale.png")
        pg.image.load("Finale.png")
        
        rect = pg.Surface((800,430), pg.SRCALPHA, 32)
        rect.fill((27, 67, 50, 40))
        SCREEN.blit(rect, (245,175))

        if HSB == True:
            end_txt = lm_font.render("You Broke The HighScore !!!", True,background_color )
            SCREEN.blit(end_txt, (280, 200))
        else:
            end_txt = lm_font.render("Game Over", True, background_color)
            SCREEN.blit(end_txt, (500, 200))

        replay_button = pg.Rect(488, 356, 324, 100)
        pg.draw.rect(SCREEN, btn, replay_button, border_radius=20)
        replay_text = lm_font.render('REPLAY', True, text_color)
        SCREEN.blit(replay_text, (505, 350))

        if replay_button.collidepoint(mouse):
            pg.draw.rect(SCREEN, btn_hover, replay_button, border_radius=20)
            SCREEN.blit(replay_text, (505, 350))
            if pg.mouse.get_pressed()[0]:
                gc.collect()
                game()

        leave_button = pg.Rect(488, 485, 324, 100)
        pg.draw.rect(SCREEN, btn, leave_button, border_radius=20)
        leave_text = lm_font.render('RETURN', True, text_color)
        SCREEN.blit(leave_text, (500, 485))

        if leave_button.collidepoint(mouse):
            pg.draw.rect(SCREEN, btn_hover, leave_button, border_radius=20)
            SCREEN.blit(leave_text, (500, 485))
            if pg.mouse.get_pressed()[0]:
                time.sleep(0.1)
                gc.collect()
                main_menu()
                
        pg.display.update()
    
    
main_menu()