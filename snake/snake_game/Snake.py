import pygame, sys, random, os

black = 0,0,0
white = 255,255,255
red = 255,0,0
green = 0,255,0

#game class to create blocks and board
class Game(): 
    def __init__(self, game_width, game_height, ai = False):
        self.game_width = game_width
        self.game_height = game_height
        self.ai = ai
        self.screen = pygame.display.set_mode((self.game_width, self.game_height))
        self.caption = pygame.display.set_caption("Slithery Snake")
        self.clock = pygame.time.Clock()
        self.seed = random.seed(self.clock)
        self.block_size = self.game_width/20
        self.player = Player(30, 30, self.block_size, self.block_size, blocks=[(30,30)], game=self)
        self.target_block = Target_Block(random.randint(0, (self.game_width-self.block_size)/30)*30, 
        random.randint(0, (self.game_width-self.block_size)/30)*30, self.block_size, self.block_size, game=self)

    def found_block(self):
        if self.target_block.x == self.player.x and self.target_block.y == self.player.y:
            return True
    
        return False


#food class for snake
class Target_Block(object):
    def __init__(self, x, y, width, height, game):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.game = game

    def get_new_block(self): 
        self.x = random.randint(0,19)*30
        self.y = random.randint(0, 19)*30

    def check_block(self): 
        for block in self.game.player.blocks: 
            if self.x > block[0]-30 and self.x < block[0]+30: 
                if self.y > block[1]-30 and self.y < block[1]+30: 
                    return False
        
        return True

#Player class to keep track of snake
class Player(object): 

    def __init__(self, x, y , width, height, blocks, game, dir='right', length=1): 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.game = game
        self.dir = dir
        self.length = length
        self.blocks =  blocks
        self.vel = width


    def move(self, dir): 
        if self.dir == 'right':
                self.x += self.vel
        elif self.dir == 'left': 
                self.x += -self.vel
        elif self.dir == 'up': 
                self.y += -self.vel
        elif self.dir == 'down': 
                self.y += self.vel
        
        self.blocks.insert(0, (self.x, self.y))
        self.blocks.pop(-1)

    def add_block(self): 

        if self.dir == 'up': 
            self.blocks.insert(0, (self.x, self.y - self.height))
        elif self.dir == 'down': 
            self.blocks.insert(0, (self.x, self.y + self.height))
        elif self.dir == 'left': 
            self.blocks.insert(0, (self.x - self.width, self.y))
        elif self.dir == 'right':
            self.blocks.insert(0, (self.x + self.width, self.y))
        
        self.x = self.blocks[0][0]
        self.y = self.blocks[0][1]
        self.length += 1

    def collision(self): 
        for i in range(1, len(self.blocks)):
            if self.blocks[i][0] == self.x and self.blocks[i][1] == self.y:
                return True
        if self.x < 0:
            return True
        if self.x > self.game.game_width - self.width:
            return True
        if self.y < 0: 
            return True
        if self.y > self.game.game_height - self.height: 
            return True
        
        return False

    def draw(self, dir):
        pygame.Surface.fill(self.game.screen, black)

        self.move(dir)

        if self.game.found_block():
            self.add_block()
            self.game.target_block.get_new_block()
            while not self.game.target_block.check_block():
                self.game.target_block.get_new_block()

        for block in self.blocks:
            pygame.draw.rect(self.game.screen, white, (block[0], block[1], self.width, self.height))

        pygame.draw.rect(self.game.screen, white, (self.game.target_block.x, self.game.target_block.y, self.game.target_block.width, self.game.target_block.height))
        pygame.display.update()




#run method to initialize and run snake game
def run():
    pygame.init()

    game = Game(600,600)
    player = game.player
    screen = game.screen
    width = game.game_width
    height = game.game_height

    # environment variables
    won = False
    lost = False

    #font and text boxes for win, lose, play again, quit
    pygame.font.init()
    font = pygame.font.Font('freesansbold.ttf', 32)
    win_text = font.render('YOU WIN!', True, white)
    lose_text = font.render('YOU LOSE!', True, black)
    play_again_text = font.render('Play Again?', True, white, black)
    quit_text = font.render("Quit", True, white, black)

    winRect = win_text.get_rect()
    winRect.center = (width//2, height//6)
    loseRect = lose_text.get_rect()
    loseRect.center = (width//2, height//6)
    playRect = play_again_text.get_rect()
    playRect.center = (width//2, height//3)
    quitRect = quit_text.get_rect()
    quitRect.center = (width//2, height//3*2)

    screen.fill(black)
    pygame.draw.rect(screen, white, (player.x, player.y, player.width, player.height))
    pygame.display.update()


    #while loop to continuously get input and perform actions on game
    while not lost and not won: 
        pygame.time.delay(200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if player.dir != 'up': 
                        player.dir = 'down'
                elif event.key == pygame.K_UP: 
                    if player.dir != 'down':
                        player.dir = 'up'
                elif event.key == pygame.K_LEFT: 
                    if player.dir != 'right':
                        player.dir = 'left'
                elif event.key == pygame.K_RIGHT: 
                    if player.dir != 'left':
                        player.dir = 'right'
        
        player.draw(player.dir)

        if player.collision():
            screen.fill(red)
            screen.blit(lose_text, loseRect)
            screen.blit(play_again_text, playRect)
            screen.blit(quit_text, quitRect)
            pygame.display.update()
            lost = True
        
        if player.length == width / player.width * height /player.height: 
            screen.fill(green)
            screen.blit(win_text, winRect)
            screen.blit(play_again_text, playRect)
            screen.blit(quit_text, quitRect)
            pygame.display.update()
            won = True

        if not game.ai: 
            while won:
                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()

                if playRect.x < mouse[0] < (playRect.x+playRect.width) and playRect.y < mouse[1] < (playRect.y+playRect.height): 
                    if click[0] == 1:
                        os.system("python3 Snake.py &")
                        break
                if quitRect.x < mouse[0] < (quitRect.x+quitRect.width) and quitRect.y < mouse[1] < (quitRect.y+quitRect.height): 
                    if click[0] == 1:
                        won = False
                        pygame.quit()
                        sys.exit()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            while lost:
                mouse = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()

                if playRect.x < mouse[0] < (playRect.x+playRect.width) and playRect.y < mouse[1] < (playRect.y+playRect.height):
                    if click[0] == 1:
                        os.system("python3 Snake.py &")
                        break
                if quitRect.x < mouse[0] < (quitRect.x+quitRect.width) and quitRect.y < mouse[1] < (quitRect.y+quitRect.height):  
                    if click[0] == 1:
                        lost = False
                        pygame.quit()
                        sys.exit()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

