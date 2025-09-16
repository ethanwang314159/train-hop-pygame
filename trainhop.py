import pygame
from pygame.locals import *
import sys
import random
import os
import json


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1024 
FPS = 60
GRAVITY_STEP = 0.5


def load_highscores():
    if os.path.exists("highscores.json"):
        with open("highscores.json", "r") as f:
            return json.load(f)
    return {"singleplayer": 0, "multiplayer": 0}

def save_highscores(data):
    with open("highscores.json", "w") as f:
        json.dump(data, f)


class Player:
    def __init__(self, x, y, left_img, right_img):
        self.x = x
        self.y = y
        self.jump = 0
        self.gravity = 0
        self.xmovement = 0
        self.direction = 0
        self.left_img = left_img
        self.right_img = right_img

    def update(self, keys, left_keys, right_keys):
        if not self.jump:
            self.y += self.gravity
            self.gravity += GRAVITY_STEP
        else:
            self.y -= self.jump
            self.jump -= GRAVITY_STEP

        for i in left_keys:
            if keys[i]:
                self.xmovement = max(self.xmovement - 1, -10)
                self.direction = 1

        for i in right_keys:
            if keys[i]:
                self.xmovement = min(self.xmovement + 1, 10)
                self.direction = 0
        else:
            self.xmovement *= 0.9 # INTERTIA!

        self.x += self.xmovement

        if self.x > SCREEN_WIDTH:
            self.x = -50
        elif self.x < -50:
            self.x = SCREEN_WIDTH

    def draw(self, screen, cameray):
        img = self.right_img if self.direction == 0 else self.left_img
        screen.blit(img, (self.x, self.y - cameray))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 100, 50)


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.autoscroll_enabled = False
        self.font = pygame.font.SysFont(None, 40)
        self.options_font = pygame.font.SysFont(None, 30)
        self.state = "info"
        self.selected = 0
        self.running = True 
        self.middle = SCREEN_WIDTH // 2 - 400

    def draw(self):
        bg = pygame.image.load("assets/backgrounds/mainmenubg.png")
        self.screen.blit(bg, (0, 0))
        titlefont = pygame.font.SysFont("freesansbold", 160)
        label = titlefont.render("   RAIN    OP", True, (0, 0, 0))
        self.screen.blit(label, (SCREEN_WIDTH // 2 - 290, SCREEN_HEIGHT // 2 + 50))

        if self.state == "main":
            pygame.display.set_caption("Train Hop - Main Menu")
            self.draw_menu(["Play", "Options", "Information", "Leaderboard", "Quit"])

        elif self.state == "play":
            pygame.display.set_caption("Train Hop - Play Menu")
            self.draw_menu(["Singleplayer", "Multiplayer", "Back"])

        elif self.state == "leaderboard":
            pygame.display.set_caption("Train Hop - Leaderboard")
            self.draw_leaderboard()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.state = "main"
                        self.selected = 0
        
        elif self.state == "options":
            pygame.display.set_caption("Train Hop - Options")
            self.draw_options()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.selected = (self.selected - 1) % 2 # TOGGLE SYSTEM
                    elif event.key == K_DOWN:
                        self.selected = (self.selected + 1) % 2

                    elif event.key == K_RETURN:
                        if self.selected == 0:
                            self.autoscroll_enabled = not self.autoscroll_enabled
                        elif self.selected == 1:
                            self.state = "main"
                            self.selected = 0
        
        elif self.state == "info":
            pygame.display.set_caption("Train Hop - Info")
            self.draw_info()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.state = "main"
                        self.selected = 0


    def draw_info(self):
        title = self.font.render("Controls Info", True, (0, 0, 0))
        self.screen.blit(title, (self.middle - title.get_width() // 2, 0))

        controls = [
            "Player Movement: Arrow keys / A-D",
            "Jump: Spacebar",
            "Pause: P",
            "Retry on pause: R",
            "Back to menu on pause: M",
            "Menu: Up/Down arrows, Enter to select",
            "PRESS ENTER TO CONTINUE"
        ]

        for i, line in enumerate(controls):
            rendered = self.options_font.render(line, True, (0, 0, 0))
            self.screen.blit(rendered, (self.middle - rendered.get_width() // 2, 50 + i * 40))

        back_text = self.font.render("Back", True, (0, 100, 200 if self.selected == 0 else 0))
        self.screen.blit(back_text, (self.middle - back_text.get_width() // 2, 350))

    def draw_leaderboard(self):
        highscores = load_highscores()
        title = self.font.render("Leaderboard", True, (0, 0, 0))
        self.screen.blit(title, (self.middle - title.get_width() // 2, 0))

        sp = self.options_font.render(f"Singleplayer: {highscores.get('singleplayer', 0)}", True, (0, 0, 0))
        mp = self.options_font.render(f"Multiplayer: {highscores.get('multiplayer', 0)}", True, (0, 0, 0))
        back = self.font.render("Back", True, (0, 100, 200 if self.selected == 0 else 0))

        self.screen.blit(sp, (self.middle - sp.get_width() // 2, 100))
        self.screen.blit(mp, (self.middle - mp.get_width() // 2, 150))
        self.screen.blit(back, (self.middle - back.get_width() // 2, 250))

    def draw_options(self):
        autoscroll_text = f"AUTOSCROLL - {'ENABLED' if self.autoscroll_enabled else 'DISABLED'}"
        back_text = "Back"
        options = [autoscroll_text, back_text]

        for i, option in enumerate(options):
            color = (0, 100, 200) if i == self.selected else (0, 0, 0)
            rendered = self.font.render(option, True, color)
            self.screen.blit(rendered, (self.middle - rendered.get_width() // 2, 200 + i * 60))

    def draw_menu(self, options):
        for i, option in enumerate(options):
            color = (0, 100, 200) if i == self.selected else (0, 0, 0)
            label = self.font.render(option, True, color)
            self.screen.blit(label, (SCREEN_WIDTH // 3 - 200, 50 + i * 60))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    self.selected += 1
                elif event.key == K_UP:
                    self.selected -= 1
                elif event.key == K_RETURN:
                    return self.select_option()

        options_count = 5 if self.state == "main" else 3 # NUMBER OF OPTIONS
        self.selected %= options_count

    def select_option(self):
        if self.state == "main":
            if self.selected == 0:
                self.state = "play"
            elif self.selected == 1:
                self.state = "options"
            elif self.selected == 2:
                self.state = "info"
            elif self.selected == 3:
                self.state = "leaderboard"
            elif self.selected == 4:
                pygame.quit()
                sys.exit()
            self.selected = 0 # RESET SELECTION

        elif self.state == "play":
            if self.selected == 0:
                return "singleplayer"
            elif self.selected == 1:
                return "multiplayer"
            elif self.selected == 2:
                self.state = "main"
            self.selected = 0 # RESET SELECTION

        elif self.state == "info":
            if self.selected == 0:
                self.state = "main"
            self.selected = 0 # RESET SELECTION

        return None

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.draw()
            result = self.handle_input()
            if result:
                return result
            pygame.display.flip()
            clock.tick(FPS)
            
class TrainHop:
    def __init__(self, mode="multiplayer", autoscroll=False):
        pygame.init()
        self.autoscroll = autoscroll
        self.paused = False
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Train Hop - " + mode.capitalize())  # Mode based window title
        self.font = pygame.font.SysFont("Arial", 25)
        self.mode = mode
        self.load_assets()
        self.setup_players()
        self.reset_game_state()

    def draw_pause_screen(self):
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  
        s.set_alpha(128)  # Semi-transparent
        s.fill((0, 0, 0))  
        self.screen.blit(s, (0, 0))  # cover the screen
        button_font = pygame.font.SysFont("Arial", 30)

        # Button dimensions and positions
        button_width = 300
        button_height = 60
        spacing = 20
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2

        return_button = pygame.Rect(center_x - button_width // 2, center_y - button_height - spacing, button_width, button_height)
        menu_button = pygame.Rect(center_x - button_width // 2, center_y + spacing, button_width, button_height)

        pygame.draw.rect(self.screen, (100, 200, 100), return_button)  # Green button
        pygame.draw.rect(self.screen, (200, 100, 100), menu_button)  # Red button

        return_text = button_font.render("Return to Game", True, (0, 0, 0))
        menu_text = button_font.render("Back to Menu", True, (0, 0, 0))
        self.screen.blit(return_text, (center_x - return_text.get_width() // 2, return_button.y + 15))
        self.screen.blit(menu_text, (center_x - menu_text.get_width() // 2, menu_button.y + 15))

        pygame.display.flip()  # Update the display

        while self.paused: # HANDLE EVENTS
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if return_button.collidepoint(event.pos):
                        pygame.mixer.music.unpause()
                        self.paused = False  # Unpause the game
                    elif menu_button.collidepoint(event.pos):
                        pygame.mixer.music.rewind()
                        self.paused = False
                        return "menu"  # Return to menu
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE or event.key == K_r:
                        pygame.mixer.music.unpause()
                        self.paused = False  # Unpause the game
                    elif event.key == K_m:
                        pygame.mixer.music.rewind()
                        self.paused = False
                        return "menu" # Return to menu

    def load_assets(self):
        load = lambda f: pygame.transform.scale(pygame.image.load(f).convert_alpha(), (100, 50))

        #  PLATFORMING IMAGES
        self.green = pygame.image.load("assets/platforming/green.png").convert_alpha()
        self.blue = pygame.image.load("assets/platforming/blue.png").convert_alpha()
        self.red = pygame.image.load("assets/platforming/red.png").convert_alpha()
        self.red_1 = pygame.image.load("assets/platforming/red_1.png").convert_alpha()
        self.red_2 = pygame.image.load("assets/platforming/red_2.png").convert_alpha()
        self.red_3 = pygame.image.load("assets/platforming/red_3.png").convert_alpha()
        self.spring = pygame.image.load("assets/platforming/spring.png").convert_alpha()
        self.spring_1 = pygame.image.load("assets/platforming/spring_1.png").convert_alpha()
        self.spike = pygame.transform.scale(pygame.image.load("assets/platforming/spike.png").convert_alpha(), (50, 50))

        # CHARACTER SPRITES
        left1 = load("assets/character sprites/train-a.png")
        left2 = load("assets/character sprites/train-b.png")
        right1 = pygame.transform.flip(left1, True, False)
        right2 = pygame.transform.flip(left2, True, False)
        self.sprite_sets = [(left1, right1), (left2, right2)]

        # LOAD SFX
        self.boing_sfx = pygame.mixer.Sound("assets/sfx/boing.wav")
        self.break_sfx = pygame.mixer.Sound("assets/sfx/break.wav")
        self.death_sfx = pygame.mixer.Sound("assets/sfx/death.wav")
        self.jump_sfx = pygame.mixer.Sound("assets/sfx/jump.wav")
        self.success_sfx = pygame.mixer.Sound("assets/sfx/success.wav")
        self.newhighscore_sfx = pygame.mixer.Sound("assets/sfx/newhighscore.wav")

        self.boing_sfx.set_volume(0.3)
        self.break_sfx.set_volume(0.3)
        self.death_sfx.set_volume(0.3)
        self.jump_sfx.set_volume(0.3)
        self.success_sfx.set_volume(0.3)
        self.newhighscore_sfx.set_volume(0.3)

        # LOAD MUSIC
        self.theme_song = pygame.mixer.music.load('assets/music/theme.wav')

    def setup_players(self):
        self.player1 = Player(SCREEN_WIDTH//2-50, SCREEN_HEIGHT-400, *self.sprite_sets[0])
        self.player2 = Player(SCREEN_WIDTH//2+50, SCREEN_HEIGHT-400, *self.sprite_sets[1])

    def reset_game_state(self):
        self.score = 0
        self.highscores = load_highscores()
        self.highscore = self.highscores.get(self.mode, 0)
        self.cameray = 0
        self.platforms = [[SCREEN_WIDTH//2-50, SCREEN_HEIGHT-300, 0, 0], [SCREEN_WIDTH//2-50, SCREEN_HEIGHT-300, 0, 0]] if self.mode != 'multiplayer' else [[SCREEN_WIDTH//2-50, SCREEN_HEIGHT-300, 0, 0], [SCREEN_WIDTH//2+50, SCREEN_HEIGHT-300, 0, 0]]
        self.springs = []
        self.spikes = []
        self.game_over = False
        self.game_over_choice = None

    def run(self):
        pygame.mixer.music.play(-1) # PLAY BACKGROUND MUSIC
        self.generatePlatforms()
        clock = pygame.time.Clock()

        while True:
            result = self.handle_events()

            if result == "menu": # RETURN TO MENU
                pygame.mixer.music.fadeout(0)
                return "menu" 
            if not self.paused:
                if self.autoscroll: self.cameray -= self.score // 10000 * 0.25 + 0.75  # AUTOSCROLLING
                
                # DRAWING THE SCREEN
                self.screen.fill((255, 255, 255))
                self.drawGrid()
                self.drawPlatforms()
                self.updatePlayers()
                self.updatePlatforms()
                self.screen.blit(self.font.render(f"Score: {self.score}", -1, (0, 0, 0)), (25, 25))

                pygame.display.flip() # UPDATE DISPLAY
                clock.tick(FPS)
                
                # UPDATE SCORE AND PLAYER POSITION - SPIKE AND SPRING AND MOVEMENT
                # CHECK FOR GAME OVER
                for player in [self.player1, self.player2]: # CHECK FOR GAME OVER AND SCORE UPDATING
                    if -1 * player.y > self.score:
                        self.score = -1 * int(player.y)
                    if (player.y - self.cameray) > SCREEN_HEIGHT:
                        if player == self.player1 or (self.mode == "multiplayer" and player == self.player2):
                            if self.score > self.highscore:
                                self.highscore = self.score
                                self.highscores[self.mode] = self.score
                                save_highscores(self.highscores)

                            choice = self.game_over_screen()
                            return choice

                    for spike in self.spikes: # SPIKE KILL
                        if player.jump <= 0 and pygame.Rect(spike[0] + (self.spike.get_width() / 4), spike[1], self.spike.get_width() * 0.25, self.spike.get_height() * 0.25).colliderect(player.get_rect()):
                            if player == self.player1 or (self.mode == "multiplayer" and player == self.player2):
                                if self.score > self.highscore:
                                    self.highscore = self.score
                                    self.highscores[self.mode] = self.score
                                    save_highscores(self.highscores)

                                self.game_over = True
                                self.game_over_choice = self.game_over_screen()
                                return self.game_over_choice
                            
                    for spring in self.springs: # SPRING BOOST BASED ON MODE
                        if pygame.Rect(spring[0], spring[1], self.spring.get_width(), self.spring.get_height()).colliderect(player.get_rect()):
                            spring[2] = 1
                            if self.mode == "multiplayer":
                                self.player1.gravity = 0
                                self.player2.gravity = 0
                                self.player1.jump = 40
                                self.player2.jump = 40
                                self.cameray -= 50
                            else:
                                player.gravity = 0
                                if player.jump >= 20:
                                    player.jump = 50
                                else:
                                    player.jump = 45
                                self.cameray -= 90
                                
                            pygame.mixer.Sound.play(self.boing_sfx)
                            

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.paused = not self.paused
                    if self.paused: # PAUSE SCREEN AND GAME AND MUSIC
                        pygame.mixer.music.pause()
                        result = self.draw_pause_screen()
                        if result == "menu":
                            return "menu"              

    def updatePlayers(self): # PLAYER MOVEMENT
        keys = pygame.key.get_pressed()
        if self.mode == "singleplayer":
            self.player1.update(keys, [K_a, K_LEFT], [K_d, K_RIGHT])
        else:
            self.player1.update(keys, [K_a], [K_d])
            self.player2.update(keys, [K_LEFT], [K_RIGHT])

        for player in [self.player1, self.player2]: # CAMERA MOVEMENT
            if player.y - self.cameray <= -100:
                self.cameray -= 45
            if player.y - self.cameray <= 100:
                self.cameray -= 35
            elif player.y - self.cameray <= 300:
                self.cameray -= 15

        self.player1.draw(self.screen, self.cameray)
        if self.mode == "multiplayer":
            self.player2.draw(self.screen, self.cameray)

    def updatePlatforms(self): # PLAYER AND PLATFORM COLLISION, PLATFORM MOVEMENT
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.green.get_width() - 10, self.green.get_height())
            for player in [self.player1, self.player2]:
                if rect.colliderect(player.get_rect()) and player.gravity and player.y < (p[1] - self.cameray): # PLAYER COLLISION WITH PLATFORM
                    if p[2] != 2: # JUMP IF NOT RED
                        player.jump = 15
                        player.gravity = 0
                        pygame.mixer.Sound.play(self.jump_sfx)
                    else: # RED PLATFORM
                        if p[3] == 0 or p[3] == 1: # IF STAGE 0 OR 1, JUMP AND RANDOMLY INCREASE STATE/DISAPPEAR
                            player.jump = 15
                            player.gravity = 0
                            pygame.mixer.Sound.play(self.jump_sfx)
                            if random.random() > 0.1:
                                p[3] += 1
                                pygame.mixer.Sound.play(self.break_sfx)
                            if p[3] == 1 and random.random() < 0.3:
                                p[3] = 3
                                pygame.mixer.Sound.play(self.break_sfx)

                        elif p[3] == 2: # IF STAGE 2, CHANCE FOR JUMP, DISAPPEAR, BIG BOOST
                            if random.random() < 0.3:
                                player.jump = 15
                                player.gravity = 0
                                pygame.mixer.Sound.play(self.jump_sfx)
                                p[3] += 1
                            elif random.random() < 0.1:
                                p[3] = 0
                            else:
                                pygame.mixer.Sound.play(self.success_sfx)
                                if self.mode == "singleplayer":
                                    player.gravity = 0
                                    player.jump = 50
                                    self.cameray -= 60
                                else:
                                    self.player1.gravity = 0
                                    self.player2.gravity = 0
                                    self.player1.jump = 40
                                    self.player2.jump = 40
                                    self.cameray -= 50
                                p[3] += 1

            if p[2] == 1: # BLUE PLATFORM MOVEMENT, BASED ON SPEED
                speed = p[4]
                if p[3] == 1:
                    p[0] += speed
                    if p[0] > SCREEN_WIDTH - 100:
                        p[3] = 0
                else:
                    p[0] -= speed
                    if p[0] <= 0:
                        p[3] = 1

    def drawPlatforms(self): # DRAWING THE PLATFORMS, SPIKES, SPRINGS, HIGH SCORE LINE, AND CREATION OF NEW PLATFORMS
        # HIGH SCORE LINE
        highscore_y = (self.highscore)
        pygame.draw.line(self.screen, (255, 255, 0), (0, -1 * (highscore_y + self.cameray)), (SCREEN_WIDTH, -1 * (highscore_y + self.cameray)), 3)
        for player in [self.player1]:
            if -1.1 * highscore_y <= player.y <= -0.9 * highscore_y:
                self.screen.blit(self.font.render("Highscore!", -1, (255, 255, 0)), (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
                pygame.mixer.Sound.play(self.newhighscore_sfx)
                if self.mode == "singleplayer":
                    player.gravity = 0
                    player.jump = 50
                else:
                    self.player1.gravity = 0
                    self.player2.gravity = 0
                    self.player1.jump = 50
                    self.player2.jump = 50
                self.cameray -= 20
            
        # DRAWING THE PLATFORMS, SPIKES, SPRINGS
        for p in self.platforms:   
            # PLATFORM CREATION         
            if self.platforms[1][1] - self.cameray > (SCREEN_HEIGHT):
                platform = random.choices([0, 1, 2], weights=[65, 50, 35])[0]

                if self.score < 30000: # SPIKE AND DIST, GRADUALLY INCREASE DIFFICULTY
                    spawnSpike = random.randint(1, 10) == 1
                    dist = self.score // 250 + 50
                elif self.score < 100000: # DIFFERENT RULE AT 30000 to 100000
                    spawnSpike = random.randint(1, 5) == 1
                    dist = self.score // 750 + 30
                else: # DIFFERENT RULE PAST 100000
                    spawnSpike = random.randint(1, 3) == 1
                    dist = self.score // 1000 + 30

                speed = random.uniform(3, 7) if platform == 1 else 0 # RULE FOR SPEED OF BLUE PLATFORM
                self.platforms.append([random.randint(0, SCREEN_WIDTH-100), self.platforms[-1][1] - dist, platform, 0, speed]) # ADD TO LIST
                coords = self.platforms[-1]

                if random.randint(0, 1000) > 900 and platform == 0: # ADD SPRING CHANCE
                    self.springs.append([coords[0] + random.randint(0, 50), coords[1] - 25, 0]) 
                if spawnSpike and (self.platforms[-1][2] != 1): # ADD SPIKE
                    self.spikes.append([coords[0] + random.randint(0, 50), coords[1] - 50, 0])
                
                self.platforms.pop(0)

            # DRAWING THE PLATFORMS
            if p[2] == 0:
                self.screen.blit(self.green, (p[0], p[1] - self.cameray))
            elif p[2] == 1:
                self.screen.blit(self.blue, (p[0], p[1] - self.cameray))
            elif p[2] == 2:
                if p[3] == 0:
                    self.screen.blit(self.red, (p[0], p[1] - self.cameray))
                elif p[3] == 1:
                    self.screen.blit(self.red_1, (p[0], p[1] - self.cameray))
                elif p[3] == 2:
                    self.screen.blit(self.red_2, (p[0], p[1] - self.cameray))
                else:
                    self.screen.blit(self.red_3, (p[0], p[1] - self.cameray))

        for spike in self.spikes: # DRAW SPIKE
            self.screen.blit(self.spike, (spike[0], spike[1] - self.cameray))

        for spring in self.springs: # DRAW SPRING
            self.screen.blit(self.spring_1 if spring[2] else self.spring, (spring[0], spring[1] - self.cameray))

    def generatePlatforms(self): # PLATFORM GENERATION AT START - SIMPLE AND EASY GUIDE
        on = SCREEN_HEIGHT+100
        while on > -500:
            x = random.randint(0, SCREEN_WIDTH-100)
            platform = random.choices([0, 1, 2], weights=[75, 50, 25])[0]
            speed = random.uniform(4, 7.5) if platform == 1 else 0
            self.platforms.append([x, on, platform, 0, speed])
            on -= 50

    def drawGrid(self): # BACKGROUND GRID
        for x in range(120):
            pygame.draw.line(self.screen, (222, 222, 222), (x * 12, 0), (x * 12, SCREEN_HEIGHT))
            pygame.draw.line(self.screen, (222, 222, 222), (0, x * 12), (SCREEN_WIDTH, x * 12))

    def game_over_screen(self): # GAME OVER
        pygame.mixer.music.fadeout(0)
        death_sfx_temp = pygame.mixer.Sound.play(self.death_sfx) # DEATH SFX
        clock = pygame.time.Clock()
        font_large = pygame.font.SysFont("Arial", 50)
        font_small = pygame.font.SysFont("Arial", 30)
        center_x = SCREEN_WIDTH // 2 
        title_y = SCREEN_HEIGHT // 4 + 100
        button_width = 200
        button_height = 50
        spacing = 20

        retry_button = pygame.Rect(center_x - button_width // 2, title_y + 150, button_width, button_height)
        menu_button = pygame.Rect(center_x - button_width // 2, retry_button.bottom + spacing, button_width, button_height)

        while True:
            bg = pygame.image.load("assets/backgrounds/background.png")
            self.screen.blit(bg, (0, 0))

            # Draw text
            game_over_text = font_large.render("Game Over", True, (0, 0, 0))
            self.screen.blit(game_over_text, (center_x - game_over_text.get_width() // 2, title_y))

            score_text = font_small.render(f"Score: {self.score}", True, (0, 0, 0))
            self.screen.blit(score_text, (center_x - score_text.get_width() // 2, title_y + 60))

            highscore_text = font_small.render(f"High Score: {self.highscore}", True, (0, 0, 0))
            self.screen.blit(highscore_text, (center_x - highscore_text.get_width() // 2, title_y + 90))

            # Draw buttons
            pygame.draw.rect(self.screen, (100, 200, 100), retry_button)
            pygame.draw.rect(self.screen, (200, 100, 100), menu_button)

            retry_text = font_small.render("Retry", True, (0, 0, 0))
            self.screen.blit(retry_text, (center_x - retry_text.get_width() // 2, retry_button.y + 10))

            menu_text = font_small.render("Menu", True, (0, 0, 0))
            self.screen.blit(menu_text, (center_x - menu_text.get_width() // 2, menu_button.y + 10))

            pygame.display.flip() # Update the display
            clock.tick(FPS)

            for event in pygame.event.get(): # BUTTON HANDLING
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_button.collidepoint(event.pos):
                        death_sfx_temp.fadeout(0)
                        return "retry"
                    elif menu_button.collidepoint(event.pos):
                        death_sfx_temp.fadeout(0)
                        return "menu"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        death_sfx_temp.fadeout(0)
                        return "retry"
                    elif event.key == pygame.K_m:
                        death_sfx_temp.fadeout(0)
                        return "menu"


def main():
    pygame.init()
    pygame.display.set_caption("Train Hop")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    menu = Menu(screen)
    while True:
        mode = menu.run()
        while mode: # MODE RETURNED BY MENU
            game = TrainHop(mode, menu.autoscroll_enabled)
            result = game.run()
            if result == "retry":
                continue  # restart same mode
            elif result == "menu":
                break     # return to menu, breaking back to menu


if __name__ == "__main__":
    main()