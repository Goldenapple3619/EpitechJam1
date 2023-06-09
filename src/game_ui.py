from .libs import *

class PainHealth(EmptyHud):
    def __init__(self: object, x: int, y: int, boss: object) -> None:
        super().__init__(x, y)
        self.boss = boss
        self.size_x = 1300 - x * 2.3
        self.size_y = 30

    def draw(self, screen):
        draw.rect(screen, (127, 15, 25), Rect(self.draw_x, self.draw_y, ((self.boss.hp3 * self.size_x) / 10000), self.size_y))
        draw.rect(screen, (127, 127, 25), Rect(self.draw_x, self.draw_y, ((self.boss.hp2 * self.size_x) / 450), self.size_y))
        draw.rect(screen, (15, 127, 25), Rect(self.draw_x, self.draw_y, ((self.boss.hp * self.size_x) / 200), self.size_y))

class Background(Tile):
    def __init__(self: object, x: int, y: int) -> None:
        super().__init__(x, y, get_image("back").convert(), 16, 1, -1)
        self.move(x, y, self.z)
        self.next = self.sprite.copy().convert()
        self.size_x = self.sprite.get_width() * 1
        self.size_y = self.sprite.get_height() * 1
        self.next_x = self.size_x + x
        self.next_y = self.size_y + y

    def update(self: object, parent: object) -> None:
        self.move(self.x - 10, self.y, self.z)
        self.next_x -= 10
        if (self.next_x + self.size_x < 1300):
            self.move(0, self.y, self.z)
            self.next_x = self.size_x
        super().update(parent)

    def move(self, x, y, z):
        self.x = x; self.draw_x = x
        self.y = y; self.draw_y = y
        self.z = z

    def draw(self: object, screen: object, cam_x: float, cam_y: float) -> None:
        super().draw(screen, cam_x, cam_y)
        if (self.x + self.size_x <= 1300):
            temp = self.sprite
            temp_x = self.draw_x
            self.move(self.next_x, self.y, self.z)
            self.sprite = self.next
            super().draw(screen, cam_x, cam_y)
            self.move(temp_x, self.y, self.z)
            self.sprite = temp