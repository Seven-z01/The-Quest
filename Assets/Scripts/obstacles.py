import pygame, random

from .settings import METEOR_SCALE
from .manager  import meteor_def, explosion_type_def
from .tools    import Sprite_sheet
from .items    import Item, Freeze


class Meteor(Sprite_sheet):

    def __init__(self, screen, player, item_group, SCREEN_W, SCREEN_H, *args):
        meteor_img, meteor_action_dict = meteor_def()
        super().__init__(meteor_img)
        self.screen = screen
        self.player = player
        self.item_group = item_group
        self.SCREEN_W = SCREEN_W
        self.SCREEN_H = SCREEN_H
        self.explosion_fx    = args[0][0]
        self.item_standby_fx = args[0][1]
        self.item_get_fx     = args[0][2]

        # Load meteor and explosion image
        self.create_animation(100, 100, meteor_action_dict)
        explosion_img, explosion_dict = explosion_type_def(1)
        self.sheet = pygame.image.load(explosion_img).convert_alpha()
        self.create_animation(100, 100, {'destroy': (6, 8, 2)})
        self.image = self.animation_dict[self.action][self.frame_index]
        # Get random meteor rect
        self.rect   = self.image.get_rect(center=(random.randint(0, self.SCREEN_W), -random.randint(0, 5000)))

        self.scale = random.randint(1, METEOR_SCALE)
        self.rect.width  = self.image.get_width()  // METEOR_SCALE
        self.rect.height = self.image.get_height() // METEOR_SCALE

        self.flip_x = random.randint(False, True)
        self.flip_y = random.randint(False, True)
        self.animation_cooldown = random.randint(10, 100)

        self.moving_x = False
        self.delta_x = 0
        self.delta_y = random.randint(1, 3)
        self.collide = False

        self.alive  = True
        self.health = self.scale * 10
        self.max_health = self.health
        self.exp = self.scale * 10

        self.freeze = Freeze(self.screen)

    def update(self, speed_y):
        # Update meteor events
        self.check_collision()
        self.check_alive()
        self.update_animation(self.animation_cooldown, 1)

        if not self.moving_x and self.rect.bottom > 0:
            if self.player.win:
                self.delta_x = self.delta_y = 0
            else:
                self.moving_x = True
                self.delta_x = random.randint(-1, 1)

        # Check if going off the edges of the screen
        if self.rect.right < 0 or self.rect.left > self.SCREEN_W or self.rect.top > self.SCREEN_H:
            self.kill() # Kill the object

        # Update rectangle position
        if not self.player.freeze:
            self.rect.x += self.delta_x
            self.rect.y += self.delta_y + speed_y
        else:
            self.freeze.update(center=(self.rect.centerx, self.rect.centery))

    # Create item
    def item_chance(self, spawn):
        chance = random.randint(0, 100)
        if chance <= spawn:
            item = Item('chance', self.screen, self.player, self.SCREEN_W, self.SCREEN_H, [self.item_standby_fx, self.item_get_fx], center=(self.rect.centerx, self.rect.centery))
            self.item_group.add(item)

    def check_collision(self):
        if self.alive and self.player.alive and not self.collide and not self.player.win:
            if abs(self.rect.centerx - self.player.rect.centerx) < self.rect.width  * self.scale and\
               abs(self.rect.centery - self.player.rect.centery) < self.rect.height * self.scale:
                self.collide = True
                self.player.collide = True
                self.player.rect.x += (self.delta_x - self.player.delta.x) * 2
                self.player.rect.y += (self.delta_y - self.player.delta.y) * 2
                if self.player.shield: self.player.shield = False
                else:
                    self.player.health -= self.scale * 10
                    self.player.less_time = False
                    self.player.freeze    = False

                self.health = 0

    def check_alive(self):
        if self.health <= 0:
            if self.alive:
                self.alive  = False
                self.health = 0
                self.speed  = 0
                self.player.dead_meteor += 1
                self.item_chance(self.scale * 10)
                self.explosion_fx.play()

            if self.player.score < self.player.score + self.exp:
                self.player.score += 1
                if self.exp > 0: self.exp -= 1

            self.animation_cooldown = self.animation_cooldown // 2
            self.update_action('destroy')
        else:
            self.update_action('turn_l')
