import pygame
import random

pygame.init()
pygame.display.set_caption("our xelnoblade chronicles at home")

scrn = (800, 600)
surface = pygame.display.set_mode(scrn)

global enemyhurt
global enemykill
global enemy_hp
global attack_time
velocity_y = 0
hp = 100

hurt_until = 0
attack_time = 100

enemyhurt = 0
enemykill = 0

sprdir = "left"
enemy_hp = 100

clock = pygame.time.Clock()


def img_load(hurtbool, enemyhurtbool, enemykill):
    global char_img
    global enemy_img

    if hurtbool:
        char_img = pygame.image.load("char_hurt.png")
    else:
        char_img = pygame.image.load("char.png")

    char_img = pygame.transform.scale(char_img, (64, 64))

    if sprdir == "right":
        char_img = pygame.transform.flip(char_img, True, False)

    if enemyhurtbool == False:
        enemy_img = pygame.image.load("enemy.png")
    else:
        enemy_img = pygame.image.load("wraith_hurt_use.png")

    enemy_img = pygame.transform.scale(enemy_img, (64, 64))


def playerhitcall():
    global enemy_hp, enemyhurt, enemykill, attack_time, current_time

    if player_hitrange.colliderect(enemy_rect):
        attack_time = pygame.time.get_ticks() + 500
        current_time = pygame.time.get_ticks()

    if attack_time != 0 and current_time >= attack_time:
        enemy_hp -= 10
        enemyhurt = True
        print(f"{enemy_hp} attacked")
    else:
        enemyhurt = False
        attack_time = 0

    if enemy_hp <= 0:
        running = False



img_load(False, enemyhurt, enemykill)

player_rect = pygame.Rect(50, 50, 64, 64)
wall_rect = pygame.Rect(700, 500, 50, 100)
enemy_rect = pygame.Rect(800, 600, 64, 64)
enemy_mask = pygame.mask.from_surface(enemy_img)
player_mask = pygame.mask.from_surface(char_img)
player_hitrange = pygame.Rect(player_rect.x, player_rect.y, 80, 80)

gravity = 0.3

running = True
while running:
    player_hitrange = pygame.Rect(player_rect.x, player_rect.y, 80, 80)

    current_time = pygame.time.get_ticks()

    # ---------------- EVENTS ----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ---------------- INPUT ----------------
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_rect.x -= 8
        sprdir = "left"

    if keys[pygame.K_RIGHT]:
        player_rect.x += 8
        sprdir = "right"

    if keys[pygame.K_UP]:
        player_rect.y -= 8

    if keys[pygame.K_SPACE]:
        player_rect.y -= 8

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            playerhitcall()

    player_rect.clamp_ip(surface.get_rect())
    enemy_rect.clamp_ip(surface.get_rect())

    # Wall bounce
    if player_rect.colliderect(wall_rect):
        velocity_y = -9

    # Enemy follows player
    if player_rect.x < enemy_rect.x:
        enemy_rect.x -= 4

    if player_rect.x > enemy_rect.x:
        enemy_rect.x += 4

    if player_rect.y < enemy_rect.y:
        enemy_rect.y -= 4

    if player_rect.y > enemy_rect.y:
        enemy_rect.y += 4

    # ---------------- COLLISION DAMAGE ----------------
    current_time = pygame.time.get_ticks()

    offset = (
        enemy_rect.x - player_rect.x,
        enemy_rect.y - player_rect.y
    )

    if player_mask.overlap(enemy_mask, offset) and current_time >= hurt_until:
        hp -= 10
        print("HP:", hp)
        hurt_until = current_time + 1500

    # gravity
    velocity_y += gravity
    player_rect.y += velocity_y

    # sprite update
    if current_time < hurt_until:
        img_load(True, enemyhurt, enemykill)
    else:
        img_load(False, enemyhurt, enemykill)

    if hp == 0:
        running = False
        print("you've died")

    # draw
    surface.fill((100, 216, 230))

    pygame.draw.rect(surface, (255, 0, 0), wall_rect)

    surface.blit(char_img, player_rect)
    surface.blit(enemy_img, enemy_rect)

    if player_rect.bottom >= scrn[1]:
        player_rect.bottom = scrn[1]
        velocity_y = 0

    clock.tick(100)
    pygame.display.flip()

pygame.quit()