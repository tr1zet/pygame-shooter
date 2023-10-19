from pygame import *
from random import * 

#Окно

window = display.set_mode((700,500))
display.set_caption('Космос Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700,500))

clock = time.Clock()
FPS = 60
#шрифт
font.init()
font = font.Font(None, 28)
win = font.render('Ну ты Доминик,красава выиграл ', True, (70, 149 , 54))
lose = font.render('Проиграл', True, (255, 0 , 0))
#музыка
mixer.init()
mixer.music.load('hh.mp3')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
#монстры и пули
monsters =sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
speed = 10
lost = 0 
lost1= 0 
#создание класса
class  GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and hero.rect.x > 5:
            hero.rect.x -= hero.speed
        if keys_pressed[K_RIGHT] and hero.rect.x < 630:
            hero.rect.x += hero.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)

class  Enemy(GameSprite):
    direction = 'down'
    def update(self):
        if self.direction == 'down':
            if self.rect.y < 500:
                self.rect.y += self.speed
            else:
                self.direction = 'up'
        elif self.direction == 'up':
            if self.rect.y > 10:
                self.rect.y -= self.speed
            else:
                self.direction = 'down'
        
        global lost
        if self.rect.y > 499:
            self.rect.y = -10
            self.rect.x = randint(10,500)
            self.speed = randint(1,2)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
            
class  Asteroid(GameSprite):
    direction = 'down'
    def update(self):
        if self.direction == 'down':
            if self.rect.y < 500:
                self.rect.y += self.speed
            else:
                self.direction = 'up'
        elif self.direction == 'up':
            if self.rect.y > 10:
                self.rect.y -= self.speed
            else:
                self.direction = 'down'     
        if self.rect.y > 499:
            self.rect.y = -10
            self.rect.x = randint(10,500)
            self.speed = randint(1,2)
            
    

#созание объектов

hero = Player('rocket.png',350,400,7)
for i in range(1,3):
    asteroid = Asteroid('asteroid.png', randint(15,500), -50, randint(1,2))
    asteroids.add(asteroid)

for i in range(1,6):
    monster = Enemy('ufo.png', randint(15,500), -50, randint(1,2))
    monsters.add(monster)
#игровой процесс
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False  
        keys_pressed = key.get_pressed()
        
        if keys_pressed[K_SPACE]:
            hero.fire()
            fire.play()
            
    
    
    
    
    
    
    sprites_list = sprite.groupcollide(monsters, bullets, True, True)
    sprites_list1 = sprite.spritecollide(hero, monsters, False)
    sprites_list2 = sprite.spritecollide(hero, asteroids, True)
    
    for  i in sprites_list:
        lost1 += 1
        monster = Enemy('ufo.png', randint(15,500), -50, randint(1,2))
        monsters.add(monster)

     

    if finish != True:
        
        window.blit(background,(0,0))
        
        
        monsters.update()
        hero.update()
        bullets.update()
        asteroids.update()
       
        hero.reset()
        bullets.draw(window)
        monsters.draw(window)
        asteroids.draw(window)
        
        text_lose = font.render('Пропущено:' +str(lost), True, (255,255,255))
        text_win = font.render('Счёт:' +str(lost1), True, (255,255,255)) #potom lost nado pom
        
        window.blit(text_lose, (40,70))
        window.blit(text_win, (40,40))
        
        
        
        if  lost1 >= 10:
            finish = True
            window.blit(win,(150,200))
        
        if  lost >= 3 or sprites_list1:
            finish = True
            window.blit(lose,(300,200))



    
    
    display.update()
    clock.tick(FPS)
    
