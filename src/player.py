from .libs import *

class HugoProjectile(Tile):
    def __init__(self, x: int, y: int, vector: tuple, speed: int, arrival: int) -> None:
        super().__init__(x, y, get_image("rondoudou"), 16, 2, 3)
        self.move(x, y, self.z)
        self.size_x = self.sprite.get_width() * 2
        self.size_y = self.sprite.get_height() * 2
        self.speed = speed
        self.vector = vector
        self.arrival = arrival
        self.angle = 0

    def move(self, x, y, z):
        self.x = x; self.draw_x = x
        self.y = y; self.draw_y = y
        self.z = z

    def update(self: object, parent: object) -> None:
        self.angle = ((self.angle + 10) % 360)
        super().update(parent)
        x = self.x + ((self.speed * self.vector[0]) / self.arrival[0]) * 60
        y = self.y + ((self.speed * self.vector[1]) / self.arrival[1]) * 60
        self.move(x, y, self.z)

    def draw(self: object, screen: object, cam_x: float, cam_y: float) -> None:
        temp = self.sprite

        self.sprite = transform.rotate(self.sprite, self.angle)

        super().draw(screen, cam_x, cam_y)

        self.sprite = temp

class Hugo(Player):
    def __init__(self: object, x: int, y: int, sprite: object, grid_size: int = 16, pixel_size: int = 3, z: int = 0, force: int = 5, health: int = 3, gravity: float = 0.4):
        super().__init__(x, y, sprite, grid_size, 4, 1, force)
        self.animation = [get_image("hugo0"), get_image("hugo1"), get_image("hugo0"), get_image("hugo2")]
        self.hp = health
        self.crouched_sprite = get_image("hugo3")
        self.gravity = gravity
        self.jumped = False
        self.crouched = False
        self.elapsed = 0
        self.projectiles = []
        self.cooldown = 0
        self.cooldown_to_put = 20
        self.inertie_move = 0
        self.inertie_jump = 0
        self.animation_part = 0
        self.animation_tick = 0
        self.ret = 0

    def reset_inertie_move(self):
        self.inertie_move = 0
        self.animation_part = 0
        self.animation_tick = 0

    def double_press(self):
        self.animation_part = 0
        self.animation_tick = 0

    def move_left(self):
        self.crouched = False
        self.ret = 1
        self.animation_tick += 1

        if (self.animation_tick == 3):
            self.animation_part += 1
            self.animation_tick = 0

        if (self.animation_part >= len(self.animation)):
            self.animation_part = 0

        if (self.inertie_move < self.force):
            self.inertie_move += self.force / 10

        self.move(self.x - self.inertie_move, self.y, self.z)

    def move_right(self):
        self.crouched = False
        self.ret = 0
        self.animation_tick += 1

        if (self.animation_tick == 3):
            self.animation_part += 1
            self.animation_tick = 0

        if (self.animation_part >= len(self.animation)):
            self.animation_part = 0

        if (self.inertie_move < self.force):
            self.inertie_move += self.force / 10

        self.move(self.x + self.inertie_move, self.y, self.z)

    def jump(self, *args):
        if (self.inertie_jump):
            self.inertie_jump -= self.force / 30
        self.move(self.x, self.y - self.inertie_jump * 2 - ((1/2)*(self.components[0].weight+self.components[0].force)*(60/60)**2), self.z)
        self.components[0].reset_force()
        self.elapsed += 1

    def crouch(self):
        self.crouched = True

    def pause(self):
        n_end = 1
        T = Text(650, 350, "Pause", (255,255,255), font.Font("./datas/fonts/HARLOWS.ttf", 32))

        T.draw(GAME.screen)
        display.flip()

        while (n_end):
            for ev in event.get():
                if ev.type == KEYDOWN:
                    if ev.key == K_ESCAPE:
                        n_end = 0
                if ev.type == QUIT:
                    GAME.running = False
                    n_end = 0
            GAME.clock.tick(60)

    def update(self, parent):
        if self.cooldown > 0: self.cooldown -= 1
        if (mouse.get_pressed()[0] and self.cooldown <= 0):
            x,y = mouse.get_pos()
            distance = sqrt((x - (self.x + self.size_x))**2 + (y - (self.y + self.size_y / 2))**2)
            self.projectiles.append(HugoProjectile(self.x + self.size_x, self.y + self.size_y / 2,
            (((x - (self.x + self.size_x)) / 60),
            ((y - (self.y + self.size_y / 2)) / 60)), 10,
            (distance,distance)))
            self.cooldown = self.cooldown_to_put

        for i, item in enumerate(self.projectiles):
            item.update(self)
            if ((item.draw_x < 0 or item.draw_x > 1300) and (item.draw_y < 0 or item.draw_y > 700)):
                self.projectiles.pop(i)

        if (self.ennemy.hp <= 0):
            self.cooldown_to_put = 16
        if (self.ennemy.hp2 <= 0):
            self.cooldown_to_put = 4

        super().update(parent)

        temp = self.y
        temp1 = self.size_y
    
        if (self.crouched):
            self.y += 9 * 4
            self.size_y -= 8
        for i, item in enumerate(self.ennemy.damage_elements):
            if ((item.x > self.x and item.y > self.y) and (item.x < self.x + self.size_x * self.pixel_size and item.y < self.y + self.size_y * self.pixel_size)
            or
            (item.x + item.size_x > self.x and item.y + item.size_y > self.y) and (item.x + item.size_x < self.x + self.size_x * self.pixel_size and item.y + item.size_y < self.y + self.size_y * self.pixel_size)):
                self.ennemy.damage_elements.pop(i)
                self.hp -= 1
        for i, item in enumerate(self.ennemy.health):

            if ((item.x > self.x and item.y > self.y) and (item.x < self.x + self.size_x * self.pixel_size and item.y < self.y + self.size_y * self.pixel_size)
            or
            (item.x + item.size_x > self.x and item.y + item.size_y > self.y) and (item.x + item.size_x < self.x + self.size_x * self.pixel_size and item.y + item.size_y < self.y + self.size_y * self.pixel_size)):
                self.ennemy.health.pop(i)
                if (self.hp != 3):
                    self.hp += 1

        for i, item in enumerate(self.ennemy.lasers):
            if (item.x < self.x + (self.size_x * self.pixel_size) / 2) and (item.x + item.size_x > self.x + (self.size_x * self.pixel_size) / 2):
                if (len(item.animation) - 1 != item.animation_part): continue
                self.ennemy.lasers.pop(i)
                self.hp -= 1
        self.y = temp
        self.size_y = temp1


    def event(self, event):
        for item in self.projectiles:
            item.event(event)

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.pause()
        super().event(event)

    def draw(self: object, screen: object, cam_x: float, cam_y: float) -> None:
        for item in self.projectiles:
            item.draw(screen, cam_x, cam_y)
        if (self.crouched):
            self.sprite = self.crouched_sprite
        else:
            self.sprite = self.animation[self.animation_part]
        if (self.ret): self.sprite = transform.flip(self.sprite, 1, 0)
        super().draw(screen, cam_x, cam_y)
        draw.rect(screen, (127, 15, 25), Rect(self.draw_x - 10, self.draw_y - 30 - (-8 * self.pixel_size if self.crouched else 0), self.size_x * self.pixel_size + 20, 5))
        draw.rect(screen, (15, 127, 25), Rect(self.draw_x - 10, self.draw_y - 30 - (-8 * self.pixel_size if self.crouched else 0), ((self.hp * (self.size_x * self.pixel_size + 20)) / 3), 5))
        self.crouched = False