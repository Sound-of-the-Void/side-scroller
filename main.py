import pygame as pg
import random

clock = pg.time.Clock()

pg.init()
screen = pg.display.set_mode((840, 480))
pg.display.set_caption('First Game')
icon = pg.image.load('images//icon.png').convert_alpha()
pg.display.set_icon(icon)

devil = pg.image.load('models//devil.png').convert_alpha()
devil_in_game = []

background = pg.image.load('images//background.jpg').convert()
walk_right = [
    pg.image.load('models//player_right//0.png').convert_alpha(),
    pg.image.load('models//player_right//1.png').convert_alpha(),
    pg.image.load('models//player_right//2.png').convert_alpha(),
    pg.image.load('models//player_right//3.png').convert_alpha()

]
walk_left = [
    pg.image.load('models//player_left//r0.png').convert_alpha(),
    pg.image.load('models//player_left//r1.png').convert_alpha(),
    pg.image.load('models//player_left//r2.png').convert_alpha(),
    pg.image.load('models//player_left//r3.png').convert_alpha()

]

player_anim_count = 0
background_x = 0

player_speed = 30
player_x = 0
player_y = 265

jump = False
jump_count = 11.5

background_sound = pg.mixer.Sound('sounds//back.mp3')
background_sound.play()

devil_respawn = pg.USEREVENT + 1
random_respawn = random.randint(2500, 4000)
pg.time.set_timer(devil_respawn, random_respawn)

text = pg.font.Font('fonts//PermanentMarker-Regular.ttf', 80)
loose_print = text.render('You Die!', False, (250, 14, 10))
restart = text.render('One more time?', False, (66, 250, 10))
restart_button = restart.get_rect(topleft=(110, 200))

fork = pg.image.load('models//fork.png').convert_alpha()
forks = []
forks_cup = 6

not_die = True

running = True

while running:

    clock.tick(10)

    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + 840, 0))

    if not_die:

        player_hitbox = walk_left[0].get_rect(topleft=(player_x - 20, player_y - 20))

        if devil_in_game:
            for (delite,element) in enumerate(devil_in_game):
                screen.blit(devil, element)
                element.x -= 20

                if element.x < -50:
                    devil_in_game.pop(delite)

                if player_hitbox.colliderect(element):
                    not_die = False

        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pg.K_RIGHT] and player_x < 590:
            player_x += player_speed
        elif keys[pg.K_LEFT] and player_x > 10:
            player_x -= player_speed

        if not jump:
            if keys[pg.K_UP]:
                jump = True
        else:
            if jump_count >= -11.5:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                jump = False
                jump_count = 11.5

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        background_x -= 4
        if background_x == -840:
            background_x = 0


        if forks:
            for (i, element) in enumerate(forks):
                screen.blit(fork, (element.x, element.y))
                element.x += 22

                if element.x > 850:
                    forks.pop(i)

                if devil_in_game:
                    for (index, devil_el) in enumerate(devil_in_game):
                        if element.colliderect(devil_el):
                            devil_in_game.pop(index)
                            forks.pop(i)


    else:
        screen.fill((188, 16, 227))
        screen.blit(loose_print, (240, 100))
        screen.blit(restart, restart_button)

        mouse = pg.mouse.get_pos()
        if restart_button.collidepoint(mouse) and pg.mouse.get_pressed()[0]:
            not_die = True
            player_x = 0
            devil_in_game.clear()
            forks.clear()
            forks_cup = 6

    pg.display.update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            pg.quit()

        if event.type == devil_respawn:
            devil_in_game.append(devil.get_rect(topleft=(850, 300)))

        if not_die and event.type == pg.KEYUP and event.key == pg.K_RETURN and forks_cup > 0:
            forks.append(fork.get_rect(topleft=(player_x + 50, player_y + 30)))
            forks_cup -= 1
