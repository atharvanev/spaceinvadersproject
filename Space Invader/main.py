########################################
#        -Space Invader-               #  
#   Author: Atharva Nevasekar          #  
#                                      #  
#   description: Space Invaders Game   #
#   using pygame                       #  
#                                      #  
#                                      #  
########################################


import pygame 
import os
import time
import random

pygame.font.init()

WIDTH = 1000
HEIGHT = 600

SCR= pygame.display.set_mode((WIDTH, HEIGHT))

playerimg = pygame.image.load("spaceinvadersproject-main\Space Invader\imgs\ship.png")  
bg = pygame.image.load("spaceinvadersproject-main\Space Invader\imgs\hills.png")
bg = pygame.transform.scale(bg, (WIDTH,HEIGHT))
invaderimg = pygame.image.load("spaceinvadersproject-main\Space Invader\imgs\enemy.png")
bullet = pygame.transform.scale(pygame.image.load("spaceinvadersproject-main\Space Invader\imgs\laser.png"), (32, 64))


class Laser:
    def __init__(self, x, y, img):  
        self.x = x+32
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def hit(self, obj):
        return collide(self, obj)
        

class Ship:
    COOLDOWN = 20

    def __init__(self,x,y,health = 50):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    
    def mov_laser(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.hit(obj):
                obj.health -= 10
                self.lasers.remove(laser)


    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x,self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width( )
    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=50):
        super().__init__(x, y, health)
        self.ship_img = playerimg
        self.laser_img = bullet
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max = health

    def mov_laser(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.hit(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)


class Invader(Ship):
    def __init__(self, x, y, health=50):
        super().__init__(x, y, health)
        self.ship_img = invaderimg
        self.laser_img = bullet
        self.mask = pygame.mask.from_surface(self.ship_img)
    def move(self, vel):
        self.y += vel

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

 

def main():
    run = True
    FPS = 60
    lives = 10
    font = pygame.font.SysFont("comicsans",25)

    enemies = []
    wave_length = 5
    ene_mov_speed = 1
    mov_speed = 7
    player = Player(500,500)
    las_mov_speed= -10

    clock = pygame.time.Clock()
    
    lost = False

    def refresh_bg():
        SCR.blit(bg,(0,0))
        lives_counter = font.render(f"Lives: {lives}",1,(255,255,255))

        

        SCR.blit(lives_counter, (15,15))

        for enemy in enemies:
            enemy.draw(SCR)

        player.draw(SCR)
        if lost:
            exit()
        pygame.display.update()
    while run:
        clock.tick(FPS)

        if lives <= 0:
            lost = True

        if len(enemies) == 0:
            wave_length += 10
            for i in range(wave_length):
                enemy = Invader((random.randrange(100, WIDTH-100)), random.randrange(-1500, -100))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - mov_speed > 0:
            player.x -= mov_speed
        if keys[pygame.K_d] and player.x + mov_speed + player.get_width() < WIDTH:
             player.x += mov_speed
        if keys[pygame.K_w] and player.y - mov_speed > 0:
            player.y -= mov_speed
        if keys[pygame.K_s] and player.y + mov_speed + player.get_height() < HEIGHT:
            player.y += mov_speed
        if keys[pygame.K_SPACE]:
            player.shoot()
        
        for enemy in enemies:
            enemy.move(ene_mov_speed)
            enemy.mov_laser(las_mov_speed, player)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.mov_laser(las_mov_speed, enemies)
        refresh_bg()


main()
