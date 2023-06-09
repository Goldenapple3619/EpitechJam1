#!/bin/python3

from src.libs import *
from src.boss import *
from src.game_ui import *
from src.game_common import *
from src.player import *
from src.classes import *
from sys import exit
from time import sleep

def return_to_main():
    GAME.objects.clear()
    GAME.hud.clear()
    GAME.collection.clear()
    GAME.shaders.clear()
    main(True)
    exit()

def credit_menu():
    GAME.objects.clear()
    GAME.hud.clear()
    GAME.collection.clear()
    GAME.shaders.clear()

    background = Tile(0, 0, get_image("menu"), 16, 1, -1)
    add_object_to_game(GAME, background)
    add_hud_to_game(GAME, ImageHud(350, 260, get_image("credit_text")))
    back_button = ImageButton(540, 600, 590 / 2.5, 211 / 2.5, get_image("exit"), return_to_main)
    add_hud_to_game(GAME, back_button)

    try:
        GAME.run()
    except KeyboardInterrupt:
        exit()
    GAME.objects.clear()
    GAME.hud.clear()
    GAME.collection.clear()
    GAME.shaders.clear()

def play_menu():
    GAME.running = True

    back = Tile(0, 0, get_image("menu"), 16, 1, -1)
    jouer_button = ImageButton(540, 300, 590 / 2.5, 211 / 2.5, get_image("play"), GAME.stop)
    exit_button = ImageButton(540, 600, 590 / 2.5, 211 / 2.5, get_image("exit"), exit)
    credit_button = ImageButton(540, 450, 590 / 2.5, 211 / 2.5, get_image("credits"), credit_menu)
    add_hud_to_game(GAME, exit_button)
    add_hud_to_game(GAME, credit_button)
    add_object_to_game(GAME, back)
    add_hud_to_game(GAME, jouer_button)

    try:
        GAME.run()
    except KeyboardInterrupt:
        exit()
    GAME.objects.clear()
    GAME.hud.clear()
    GAME.collection.clear()
    GAME.shaders.clear()

def win_menu():
    GAME.objects.clear()
    GAME.hud.clear()
    GAME.collection.clear()
    GAME.shaders.clear()
    mixer.music.unload()
    GAME.running = True

    back = Tile(0, 0, get_image("menu_win"), 16, 1, -1)
    back_button = ImageButton(540, 600, 590 / 2.5, 211 / 2.5, get_image("exit"), return_to_main)
    credit_button = ImageButton(540, 500, 590 / 2.5, 211 / 2.5, get_image("credits"), credit_menu)
    add_hud_to_game(GAME, back_button)
    add_hud_to_game(GAME, credit_button)
    add_object_to_game(GAME, back)

    try:
        GAME.run()
    except KeyboardInterrupt:
        exit()

def lose_menu():
    GAME.objects.clear()
    GAME.hud.clear()
    GAME.collection.clear()
    GAME.shaders.clear()
    mixer.music.unload()
    GAME.running = True

    back = Tile(0, 0, get_image("menu_lose"), 16, 1, -1)
    back_button = ImageButton(540, 600, 590 / 2.5, 211 / 2.5, get_image("exit"), return_to_main)
    credit_button = ImageButton(540, 500, 590 / 2.5, 211 / 2.5, get_image("credits"), credit_menu)
    add_hud_to_game(GAME, back_button)
    add_hud_to_game(GAME, credit_button)
    add_object_to_game(GAME, back)

    try:
        GAME.run()
    except KeyboardInterrupt:
        exit()

def play_game():
    mixer.music.load("./datas/music/theme.mp3")
    GAME.running = True

    hugo = Hugo(500, 500, get_image("hugo0"), force=10, health=3)
    boss = Boss(800, 50, get_image("pain"), 500, hugo)
    add_object_to_game(GAME, hugo)
    add_object_to_game(GAME, boss)
    add_object_to_game(GAME, Background(0,0))

    add_hud_to_game(GAME, PainHealth(50, 10, boss))

    hugo.add_component(lambda parent: RigidBody(parent, 0))
    add_script_to_game(GAME, lambda *args: check_grounded(hugo, *args))
    add_action_to_player(hugo, check_jump, hugo.jump)
    add_action_to_player(hugo, lambda p, k: k[K_s], lambda *args: hugo.crouch())
    add_action_to_player(hugo, lambda p, k: k[K_d] and p.x <= 900 - p.size_x * 3, lambda *args: hugo.move_right())
    add_action_to_player(hugo, lambda p, k: k[K_q] and p.x > 0, lambda *args: hugo.move_left())
    add_action_to_player(hugo, lambda p, k: not k[K_q] and not k[K_d], lambda *args: hugo.reset_inertie_move())
    add_action_to_player(hugo, lambda p, k: k[K_q] and k[K_d], lambda *args: hugo.double_press())

    add_script_to_game(GAME, lambda *args: check_end(hugo, boss, *args))

    GAME.state = -1

    mixer.music.play(loops=-1)

    try:
        GAME.run()
    except KeyboardInterrupt:
        return (130)
    if GAME.state == 1:
        win_menu()
    else:
        lose_menu()

def main(inited = False) -> int:

    if not inited:
        init_engine()
        add_camera_to_game(GAME, CAMERA)

    display.set_icon(get_image("pain"))

    play_menu()
    play_game()

    return (0)

if __name__ == "__main__":
    exit(main())

#todo fix zero division on projectiles