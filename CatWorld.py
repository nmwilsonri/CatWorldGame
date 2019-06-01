""" CatWorld.py
    This is a playable version
    of the game. It keeps track of score
    and of lives. If you win it presents a
    winning screen. If you lose there is a game over
    screen.
    Nate Wilson
"""

import pygame, random, CatWorldSprites
pygame.init()
from pygame.math import Vector2 as vector

#sound
if not pygame.mixer:
    print "problem with sound"
else:
    pygame.mixer.init()

TREATS = 10

#display
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Cat World")
pygame.mixer.music.load("mozart.ogg")
pygame.mixer.music.play(-1)

def gameOver():
    background = pygame.Surface(screen.get_size())    
    background.fill((255,255,0))
    font = pygame.font.SysFont("Comic Sans MS", 30)
    text = font.render("Game Over",1, (255,0,0))
    screen.blit(background, (0,0))
    screen.blit(text, (250,250))

def youWin():
    background = pygame.Surface(screen.get_size())    
    background.fill((255,255,0))
    font = pygame.font.SysFont("Comic Sans MS", 30)
    text = font.render("You Win!",1, (255,0,0))
    screen.blit(background, (0,0))
    screen.blit(text, (250,250))

def main():
    points = 0
    #entities
    background = pygame.image.load("bg.png")  
    screen.blit(background, (0,0))

    # Player
    moose = CatWorldSprites.HeroCat(screen)
    
    # Scoreboard
    scoreboard = CatWorldSprites.ScoreBoard(screen)
    scoreSprite = pygame.sprite.Group(scoreboard)

    # Enemies
    enemies = []
    for i in range(3):
        enemy = CatWorldSprites.EnemyCat(screen)
        enemies.append(enemy)
  
    # Platforms
    ground = CatWorldSprites.Platforms(screen,860,40,0,440)
    platform1 = CatWorldSprites.Platforms(screen,200,40,100,340)
    platform2 = CatWorldSprites.Platforms(screen,200,40,340,240)
    platform3 = CatWorldSprites.Platforms(screen,200,40,80,140)
    platformGroup = pygame.sprite.Group(ground,platform1,platform2,platform3)

    # Treats
    treats = []
    for i in range(TREATS):
        treat = CatWorldSprites.Treats(screen)
        treats.append(treat)
        
    # SPrite Groups
    player = pygame.sprite.Group(moose)
    treatGroup = pygame.sprite.Group(treats)
    allsprites = pygame.sprite.Group(moose,enemies,treats,ground,platform1,platform2,platform3)
    enemyGroup = pygame.sprite.Group(enemies)

    keepGoing = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    
    #game loop
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    moose.jump()

        if moose.vel.y > 0:
            platformCollisions = pygame.sprite.spritecollide(moose, platformGroup,False)
            if platformCollisions:
                moose.pos.y = platformCollisions[0].rect.top
                moose.vel.y = 0

        enemyHeroCollision = pygame.sprite.spritecollide(moose, enemyGroup, False)
        if enemyHeroCollision:
            moose.lives -= 1
            moose.pos = vector(400,400)
            moose.rawr()
            scoreboard.lives = moose.lives

                          
        platformGroup.update(screen)
        treatGroup.update(screen)
        allsprites.update(screen)
        enemyGroup.update(screen)
        scoreSprite.update(screen)

        #update the screen
        platformGroup.clear(screen, background)
        treatGroup.clear(screen, background)
        allsprites.clear(screen, background)
        enemyGroup.clear(screen, background)
        scoreSprite.clear(screen, background)

        platformGroup.draw(screen)
        allsprites.draw(screen)
        treatGroup.draw(screen)
        enemyGroup.draw(screen)
        scoreSprite.draw(screen)

        
        treatCollisions = pygame.sprite.spritecollide(moose, treatGroup, True)
        if treatCollisions:
            points += 1
            scoreboard.score = points
            scoreSprite.update(screen)
            moose.eat()

        if points == 10:
            youWin()
        
        if moose.lives < 0:
            gameOver()

        font = pygame.font.SysFont("Comic Sans MS", 20)
        text = font.render("Space to Jump arrow keys to move",1, (255,0,0))
        screen.blit(text, (100,440))

        pygame.display.flip()
    pygame.quit();

if __name__ == "__main__":
    main()
