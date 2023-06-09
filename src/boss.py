from .libs import *
from random import randint

class ChocoLaser(Tile):
    def __init__(self, x: int, y: int, speed: int) -> None:
        super().__init__(x, y, get_image("choco_laser_pre10"), 16, 1, 3)
        self.move(x, y, self.z)
        self.size_x = self.sprite.get_width() * 1
        self.size_y = self.sprite.get_height() * 1
        self.speed = speed
        self.hp = 1
        self.animation_part = 0
        self.animation_elapsed = 0
        self.animation = [get_image("choco_laser_pre9"), get_image("choco_laser_pre8"), get_image("choco_laser_pre7"), get_image("choco_laser_pre6"), get_image("choco_laser_pre5"), get_image("choco_laser_pre4"), get_image("choco_laser_pre3"), get_image("choco_laser_pre2"), get_image("choco_laser_pre1"), get_image("choco_laser_pre0"), get_image("choco_laser")]

    def move(self, x, y, z):
        self.x = x; self.draw_x = x
        self.y = y; self.draw_y = y
        self.z = z

    def update(self: object, parent: object) -> None:
        self.animation_elapsed += 1
        if (self.animation_elapsed == self.speed and self.animation_part != len(self.animation) - 1):
            self.animation_part += 1
            self.animation_elapsed = 0
            self.sprite = self.animation[self.animation_part]
        if (self.animation_elapsed == self.speed * 5):
            self.hp = 0
        super().update(parent)


    def draw(self: object, screen: object, cam_x: float, cam_y: float) -> None:
        super().draw(screen, cam_x, cam_y)

class Regen(Tile):
    def __init__(self, x: int, y: int, speed: int) -> None:
        super().__init__(x, y, get_image("coeur"), 16, 2, 3)
        self.move(x, y, self.z)
        self.speed = speed
        self.size_x = self.sprite.get_width() * 1
        self.size_y = self.sprite.get_height() * 1

    def move(self, x, y, z):
        self.x = x; self.draw_x = x
        self.y = y; self.draw_y = y
        self.z = z

    def update(self: object, parent: object) -> None:
        super().update(parent)
        x = self.x - self.speed
        self.move(x, self.y, self.z)

    def draw(self: object, screen: object, cam_x: float, cam_y: float) -> None:
        super().draw(screen, cam_x, cam_y)

class ChocoShroom(Tile):
    def __init__(self, x: int, y: int, speed: int, enemmy_projectiles: list, hp: int) -> None:
        super().__init__(x, y, get_image("choco_shroom" if hp <= 5 else "choco_shroom_hat"), 16, 3, 3)
        self.move(x, y - 25 if hp > 5 else y, self.z)
        self.size_x = self.sprite.get_width() * 3
        self.size_y = self.sprite.get_height() * 3
        self.speed = speed
        self.enemmy_projectiles = enemmy_projectiles
        self.hp = hp

    def move(self, x, y, z):
        self.x = x; self.draw_x = x
        self.y = y; self.draw_y = y
        self.z = z

    def update(self: object, parent: object) -> None:
        super().update(parent)
        x = self.x - self.speed
        self.move(x, self.y, self.z)

        for i, item in enumerate(self.enemmy_projectiles):
            if ((item.x > self.x and item.y > self.y) and (item.x < self.x + self.size_x and item.y < self.y + self.size_y)
            or (item.x + item.size_x > self.x and item.y + item.size_y > self.y)
            and (item.x + item.size_x < self.x + self.size_x and item.y + item.size_y < self.y + self.size_y)):
                self.enemmy_projectiles.pop(i)
                self.hp -= 1
                if (self.hp == 5):
                    self.sprite = get_image("choco_shroom")
                    self.size_x = self.sprite.get_width() * 3
                    self.size_y = self.sprite.get_height() * 3
                    self.draw_size_x = self.size_x
                    self.draw_size_y = self.size_y
                    self.move(self.x, self.y + 25, self.z)

    def draw(self: object, screen: object, cam_x: float, cam_y: float) -> None:
        super().draw(screen, cam_x, cam_y)

class PainPepite(Tile):
    def __init__(self, x: int, y: int, speed: int) -> None:
        super().__init__(x, y, get_image("pepite"), 16, 3, 3)
        self.move(x, y, self.z)
        self.add_component(lambda *args: RigidBody(self, 0.05, 5))
        self.size_x = self.sprite.get_width() * 3
        self.size_y = self.sprite.get_height() * 3
        self.speed = speed
        self.angle = 0
        self.to = randint(100, 400) / 100
        
    def move(self, x, y, z):
        self.x = x; self.draw_x = x
        self.y = y; self.draw_y = y
        self.z = z

    def update(self: object, parent: object) -> None:
        clock = 0
        self.angle = ((self.angle + 10) % 360)
        super().update(parent)
        while (clock < self.to):
            self.move(self.x - 0.01, self.y - 0.01, self.z)
            clock += 0.01

    def draw(self: object, screen: object, cam_x: float, cam_y: float) -> None:
        temp = self.sprite

        self.sprite = transform.rotate(self.sprite, self.angle)

        super().draw(screen, cam_x, cam_y)

        self.sprite = temp

class Boss(Tile):
    def __init__(self: object, x: int, y: int, sprite: object, hp: int, player: object): 
        super().__init__(x, y , sprite, 16, 1, 0)
        self.temp_y = y
        self.player = player
        self.sprite_2 = get_image("pain2")
        self.sprite_3 = get_image("pain3")
        self.projectiles_ennemy = player.projectiles
        self.hp = 200
        self.hp2 = 450
        self.hp3 = 10000
        self.size_x = self.sprite.get_width() * 1
        self.size_y = self.sprite.get_height() * 1
        self.move(x, y, self.z)
        self.cooldown = 100
        self.cooldown2 = 230
        self.elapsed = 0
        self.elapsed2 = 0
        self.damage_elements = []
        self.attacks = (self.choco_shoot,)
        player.ennemy = self
        self.movement = 0
        self.direction = 1
        self.health = []
        self.lasers = []

    def choco_shroom(self):
        self.damage_elements.append(ChocoShroom(1300, 600 - 16 * 3, 2, self.projectiles_ennemy, 5))

    def choco_shroom_reinforced(self):
        self.damage_elements.append(ChocoShroom(1300, 600 - 16 * 3, 2, self.projectiles_ennemy, 15))

    def choco_laser(self):
        self.lasers.append(ChocoLaser((self.player.draw_x + self.player.draw_size_x / 2) - 66, 0, 20))

    def choco_shoot(self):
        self.damage_elements.append(PainPepite(self.x, self.y + self.size_y / 2, 2))

    def update(self: object, parent: object) -> None:
        if (self.direction == 1 and self.movement >= 10):
            self.direction = -1
        elif (self.direction == -1 and self.movement <= 0):
            self.direction = 1
        if (self.direction == 1):
            self.movement += 0.3
        elif (self.direction == -1):
            self.movement -= 0.3
        self.move(self.x, self.temp_y + self.movement, self.z)
        self.elapsed2 += 1
        if (self.elapsed2 > self.cooldown2 and (self.hp2 <= 0)):
            self.elapsed2 = 0
            self.choco_laser()
        self.elapsed += 1
        if (self.elapsed > self.cooldown):
            self.elapsed = 0
            self.attacks[randint(0, len(self.attacks) - 1)]()
        for i, item in enumerate((*self.damage_elements, *self.health, *self.lasers)):
            item.update(self)
            if (item.draw_x < 0 or item.draw_x > 1300) and (item.draw_y < 0 or item.draw_y > 700):
                self.damage_elements.pop(i)
        super().update(parent)
        for i, item in enumerate(self.projectiles_ennemy):
            if ((item.x > self.x + 30 and item.y > self.y + 30) and (item.x < self.x + self.size_x - 30 and item.y < self.y + self.size_y - 30)
            or
            (item.x + item.size_x > self.x + 30 and item.y + item.size_y > self.y + 30) and (item.x + item.size_x < self.x + self.size_x - 30 and item.y + item.size_y < self.y + self.size_y - 30)):
                self.projectiles_ennemy.pop(i)
                if (self.hp3 <= 5000):
                    self.cooldown2 = 200
                if (self.hp3 <= 1000):
                    self.cooldown2 = 150
                if (self.hp2 <= 0):
                    self.hp3 -= 5
                elif (self.hp <= 0):
                    self.hp2 -= 5
                else:
                    self.hp -= 5
        if (self.hp2 <= 0):
            self.sprite = self.sprite_3
            self.cooldown = 65
            self.attacks = (self.choco_shoot, self.choco_shroom_reinforced)
        elif (self.hp <= 0):
            self.sprite = self.sprite_2
            self.cooldown = 90
            self.attacks = (self.choco_shoot, self.choco_shroom)

        for i, item in enumerate(self.damage_elements):
            if (type(item).__name__ == "ChocoShroom" and item.hp <= 0):
                at = self.damage_elements.pop(i)
                proba_spawn = randint(0, 19)
                if (proba_spawn <= 0):
                    self.health.append(Regen(at.draw_x, at.draw_y, 2))

        for i, item in enumerate(self.lasers):
            if (item.hp <= 0):
                self.lasers.pop(i)
                continue

    def move(self, x, y, z):
        self.x = x; self.draw_x = x
        self.y = y; self.draw_y = y
        self.z = z

    def draw(self: object, screen: object, cam_x: float, cam_y: float) -> None:
        super().draw(screen, cam_x, cam_y)
        for item in (*self.damage_elements, *self.health, *self.lasers):
            item.draw(screen, cam_x, cam_y)