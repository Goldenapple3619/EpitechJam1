from .constants import *
from .libs import *
from .load_prefabs import *
from .constants import *
from .classes import *

def check_grounded(hugo, *args) -> None:
    if (hugo.y + hugo.size_y * hugo.pixel_size >= 600):
        hugo.move(hugo.x, 600 - hugo.size_y * hugo.pixel_size, hugo.z)
        hugo.components[0].reset_force()
        hugo.jumped = False
        hugo.elapsed = 0
        hugo.inertie_jump = hugo.force

def check_jump(p, k):
    if (not k[K_z] and not k[K_SPACE]):
        p.jumped = True
    return (k[K_z] or k[K_SPACE]) and p.elapsed < 20 and not p.jumped

def check_end(p, b, *args):
    if (p.hp <= 0 or b.hp3 <= 0):
        GAME.state = (0 if p.hp <= 0 else 1)
        GAME.running = False

def free_cam():
    keys=get_pressed()

    if not keys[K_f]: return
    while 1:
        event.get()
        keys=get_pressed()
    
        if keys[K_ESCAPE]:
            break
        if keys[K_LEFT]:
            CAMERA.x -= 10.5
        if keys[K_UP]:
            CAMERA.y -= 10.5
        if keys[K_RIGHT]:
            CAMERA.x += 10.5
        if keys[K_DOWN]:
            CAMERA.y += 10.5
        GAME.draw()
        GAME.clock.tick(GAME.fps)
    CAMERA.x = 0
    CAMERA.y = 0

def create_map():
    maps = GLD(f"./datas/maps/map{randint(0,4)}.gld", GAME)
    maps.lexer()
    maps.interpret()
