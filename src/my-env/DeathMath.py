import random
import pygame
import os
import sys

def chooseTip():
  tips = ['Tip: Don\'t repeat the same signs, your score will decrease', 'Tip: Each sign have a specific weight: + is 2, - is 4, * is 6 and / is 8', 'Tip: You can shoot if your score is greater than 0']
  return tips[random.randint(0, len(tips) - 1)]
    ## MATH EXPRESSION
def checkExpression():
  expression_converted = eval(expression_text)
  
  return expression_converted

def sumPoints(expression):
  singsOfSum = expression.count('+')
  sum = 0
  weight = 2
  while(singsOfSum != 0):
    sum += weight
    singsOfSum -= 1
    if weight != 1:
      weight -= 1
  return sum

def subPoints(expression):
  singsOfSub = expression.count('-')
  sub = 0
  weight = 4
  while(singsOfSub != 0):
    sub += weight
    singsOfSub -= 1
    if weight != 1:
      weight -= 1
  return sub

def multiplicationPoints(expression):
  singsOfMul = expression.count('*')
  mul = 0
  weight = 6
  while(singsOfMul != 0):
    mul += weight
    singsOfMul -= 1
    if weight != 1:
      weight -= 1
  return mul

def dividePoints(expression):
  singsOfDiv = expression.count('/')
  div = 0
  weight = 8
  while(singsOfDiv != 0):
    div += weight
    singsOfDiv -= 1
    if weight != 1:
      weight -= 1
  return div

pygame.init()
pygame.display.set_caption('Death Math')
clock = pygame.time.Clock()

height = 700
width = 1320

ROOF_NUMBER = 10000

screen = pygame.display.set_mode([width, height], pygame.RESIZABLE)

bullet_font = pygame.font.Font(None, 32)
random_font = pygame.font.Font(None, 100)
expression_font = pygame.font.Font(None, 80)
game_over_message = 'Game Over. Press any key to play again'
game_over_font = pygame.font.Font(None, 30)

user_text = ''
tip = ''
score = 0

expression_rect = pygame.Rect(200, 200, 140, 32)

keys_list = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_KP0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5, pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9, pygame.K_KP0, pygame.K_KP_DIVIDE, pygame.K_KP_MULTIPLY, pygame.K_KP_MINUS, pygame.K_KP_PLUS, pygame.K_ASTERISK, pygame.K_PLUS, pygame.K_MINUS, pygame.K_BACKSPACE, pygame.K_BACKSPACE, pygame.K_SLASH, pygame.K_PLUS]

random_number = random.randint(1, 100)

expression_result = ''
expression_text = ''

bullets = 0
shoot = False
 
dir_index = os.path.dirname(__file__)
bg_img = pygame.image.load(os.path.join(dir_index, 'media','images','scene', 'cemitery-background.png'  ))
bg_img = pygame.transform.scale(bg_img,(width, height))
zombie_img = pygame.image.load(os.path.join(dir_index, 'media','images','sprites', 'spritesheet.png'  ))
player_img = pygame.image.load(os.path.join(dir_index, 'media','images','sprites', 'soldier.png'  ))
bullet_img = pygame.image.load(os.path.join(dir_index, 'media','images','sprites', '21.png'  ))
bg_game_over = pygame.image.load(os.path.join(dir_index, 'media','images','scene', 'game_over.png'))
bg_game_over = pygame.transform.scale(bg_game_over, (width, height))

pygame.mixer.music.set_volume(0.6 )
bg_sound = pygame.mixer.music.load(os.path.join(dir_index, 'media', 'sounds', 'AHa-8Bit-On-Me-Take-On-Me-8-Bit.wav'))
pygame.mixer.music.play(-1)

zombies_sound = pygame.mixer.Sound(os.path.join(dir_index, 'media', 'sounds', 'zombies_sound.wav'))
fail_sound = pygame.mixer.Sound(os.path.join(dir_index, 'media', 'sounds', 'fail_Sponge_Bob.wav'))
shot_sound = pygame.mixer.Sound(os.path.join(dir_index, 'media', 'sounds', 'Realistic-Gunshot-Sound-Effect.wav'))

sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()

game_over = False
class Bullet(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.transform.scale(bullet_img, (76, 40))
    self.rect = self.image.get_rect()
    self.mask = pygame.mask.from_surface(self.image)
    self.rect.center = (200, 577)

  def update(self):
    self.rect.x += 8

  def destroy(self):
    self.kill()

class Player(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self) 
    self.player_images = []
    for i in range (1, 4):
      img = player_img.subsurface((i * 64, 0), (64, 64))
      img = pygame.transform.scale(img, (64 * 2, 64 * 2))
      self.player_images.append(img)

    self.index_lista = 0
    self.image = self.player_images [self.index_lista]
    self.rect = self.image.get_rect()
    self.mask = pygame.mask.from_surface(self.image)
    self.rect.center = (120, 588)

  def update (self):
    if self.index_lista > 1:
        self.index_lista = 0
    self.index_lista += 0.1
    self.image = self.player_images[int(self.index_lista)]

class Zombie(pygame.sprite.Sprite):
  def __init__(self, column):
    pygame.sprite.Sprite.__init__(self) 
    self.zombies_image = []
    for i in range (4):
      img = zombie_img.subsurface((i * 270, 270 * column), (270, 270))
      img = pygame.transform.scale(img, (185, 185))
      self.zombies_image.append(img)

    self.index_lista = 0
    self.image = self.zombies_image [self.index_lista]
    self.maks = pygame.mask.from_surface(self.image)
    self.rect = self.image.get_rect()
    self.rect.center = (1100 + column * 120,558)

  def update(self):
    if self.index_lista > 3:
        self.index_lista = 0
    self.index_lista += 0.1
    self.image = self.zombies_image[int(self.index_lista)]
    self.rect.x -= 0.5

player = Player()

player_sprites.add(player)

pygame.mouse.set_visible(False)

enemies_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemies_timer, 1500)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

    ## KEYS PRESSED

    if game_over:
      if event.type == pygame.KEYDOWN:
        enemies.empty()
        game_over = False
        tip_activate = True
        bullets = 0
        expression_text = ''
        score = 0
        
    else:
      if event.type == pygame.KEYDOWN:
        if (event.key) in keys_list:
          if event.key == pygame.K_BACKSPACE:
            expression_text = expression_text[:-1]

          else:
            expression_text += event.unicode

        if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:

          if (not len(expression_text.strip()) == 0):
            expression_result = checkExpression()

          if random_number == expression_result:
            bullets += sumPoints(expression_text) + subPoints(expression_text) + multiplicationPoints(expression_text) + dividePoints(expression_text)
          expression_text = ''
          random_number = random.randint(1, ROOF_NUMBER)
      
        if event.key == pygame.K_SPACE:
          shoot = True

      if event.type == pygame.KEYUP:
        if event.key == pygame.K_SPACE:
          shoot = False
          if bullets > 0:
            bullet_sprites.add(Bullet())
            shot_sound.play()
            bullets -= 1

      if event.type == enemies_timer:
        enemies.add(Zombie(random.randint(1, 3)))

  if game_over:
    screen.fill((0, 0, 0))
    screen.blit(bg_game_over, (0, 0))

    game_over_text = game_over_font.render(game_over_message, True, (200,0,0))
    screen.blit(game_over_text, ( 460, 600))

    score_text = bullet_font.render(f'score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (80, 50))

    tips_text = game_over_font.render(tip, True, (200,0,0))
    screen.blit(tips_text, ( 400, 650))

  else:
    zombieHitted = pygame.sprite.groupcollide(enemies, bullet_sprites, True, True)
    playerHitted = pygame.sprite.spritecollideany(player, enemies, None)

    if zombieHitted:
      zombies_sound.play()
      score += 1
    if playerHitted:
      tip = chooseTip()
      fail_sound.play()
      game_over = True

    screen.blit(bg_img, (0, 0))
              ######### TEXTS IN SCREEN ############

    ## EXPRESSION LABEL
    text_expression = expression_font.render(expression_text, True, (255,255,255))
    screen.blit(text_expression, (360, 140))

    ## RANDOM NUMBER TEXT
    random_text = random_font.render((str(random_number).encode('utf-8').decode('utf-8')), True, (200, 55, 100))
    screen.blit(random_text, (580, 20))

    ## BULLET TEXT
    bullets_text = bullet_font.render((str(bullets).encode('utf-8').decode('utf-8')), True, (255,255,255))
    screen.blit(bullets_text, (80, 52))

    # SCORE TEXT
    score_text = bullet_font.render(f'score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (160, 50))


    enemies.draw(screen)
    enemies.update()
    player_sprites.draw(screen)
    player_sprites.update()
    bullet_sprites.draw(screen)
    bullet_sprites.update()

  pygame.display.flip()
  clock.tick(60)