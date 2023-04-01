#1 Import Things
from pygame import *
from random import randint
from random import choice
#2 Create window + clock
window = WIDTH, HEIGHT = 800, 500
window = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
score = 0
font.init()
mixer.init()
#3 Get base classes
class ImageSprite(sprite.Sprite):
    # constructor function. Runs ONCE every time a new object it's created
    def __init__(self, filename, pos, size, player_speed):
        super().__init__()
        self.image = image.load(filename)
        self.image = transform.scale(self.image, size)
        self.rect = Rect(pos, size)
        self.initial_pos = pos
        self.speed = player_speed
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
    def reset(self):
        self.rect.topleft = self.initial_pos
 
class PlayerSprite(ImageSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d]:
            self.rect.x += 8
        if keys[K_a]:
            self.rect.x -= 8

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH   
    def shoot(self):
        b = BulletSprite(filename = "bullet.png", pos = (0,0), size = (7,12), player_speed = 20)
        b.rect.center = self.rect.midtop
        bullets.add(b)

class EnemySprite(ImageSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = randint(100, 700)
            self.rect.bottom  = 0

class TextSprite():
    def __init__(self, text, color, pos, font_size):
        self.font = font.Font(None, font_size)
        self.pos = pos
        self.color = color
        self.set_new_text(text)
    def set_new_text(self, new_text):
        self.image = self.font.render(new_text, True, self.color)
    def draw(self, surface):
        surface.blit(self.image, self.pos)

class BulletSprite(ImageSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

points_counter = TextSprite(text = "Score: " + str(score), color=(184, 220, 255), pos = (50,50), font_size = 60)

bg = ImageSprite('BG.png', pos=(0, 0), size=(WIDTH, HEIGHT),player_speed=0)
player = PlayerSprite('Player.png', pos=(800, 400), size=(70, 70), player_speed=0)
player.rect.bottom = HEIGHT-5
shooting_sound = [mixer.Sound('S1.mp3'), mixer.Sound('S2.mp3'), mixer.Sound('S3.mp3'), mixer.Sound('S4.mp3'), mixer.Sound('S5.mp3'), mixer.Sound('S6.mp3'), mixer.Sound('S7.mp3'), mixer.Sound('S8.mp3'), mixer.Sound('S9.mp3'), mixer.Sound('S10.mp3'),]
oof = mixer.Sound('Cool.mp3')

# enemy = EnemySprite('Enemy.png', pos=(0, 0), size=(100, 100))
# enemy_2 = EnemySprite('Enemy.png', pos=(500, 0), size = (100, 100))
monsters = sprite.Group()
bullets = sprite.Group()
for a in range(1,5):
    enemy = EnemySprite('Enemy.png', pos=(randint(0,800), 0), size=(100, 100), player_speed=randint(1, 6))
    monsters.add(enemy)

# monsters = sprite.Group()
# for a in range(20,30):
#     enemy = EnemySprite('Enemy.png', pos=(randint(0,1500), 0), size=(100, 100))
#     monsters.add(enemy)
state = "Initializing" 
game_over = False
win_img = ImageSprite('HI_hi.png', pos=(0, 0), size=(WIDTH, HEIGHT), player_speed=0)
lose_img = ImageSprite('L_Bozo.jpg', pos=(0, 0), size=(WIDTH, HEIGHT), player_speed=0)
while not event.peek(QUIT):
    if not game_over:
        for e in event.get():
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    player.shoot()
                    sound_effect = choice(shooting_sound)
                    sound_effect.play()
        player.update()
        # enemy.update()
        # enemy_2.update()
        bg.draw(window)
        player.draw(window)
        
        monsters.draw(window)
        bullets.draw(window)
        monsters.update()
        bullets.update()
        player_hits = sprite.spritecollide(player, monsters, True)
        for hit in player_hits:
            score -= 50000000
            points_counter.set_new_text("Score: " + str(score))
            enemy = EnemySprite('Enemy.png', pos=(randint(0,800), 0), size=(100, 100), player_speed=randint(1, 6))
            monsters.add(enemy)


        enemy_hits = sprite.groupcollide(bullets, monsters, True, True)
        for hit in enemy_hits:
            score += 500000000
            points_counter.set_new_text("Score: " + str(score))
            oof.play()
            
            
            enemy = EnemySprite('Enemy.png', pos=(randint(0,800), 0), size=(100, 100), player_speed=randint(1, 6))
            monsters.add(enemy)
        # enemy.draw(window)
        # enemy_2.draw(window)
        points_counter.draw(window)
        if score >= 10000000000:
            game_over = True
            state = 'WIN'
        elif score <= -10000000:
            game_over = True
            state = 'L'
    else:
        if state == 'WIN':
            win_img.draw(window)
        elif state == "L":
            lose_img.draw(window)
        

#7 Update display
    display.update()
#8 clock tick
    clock.tick(60)