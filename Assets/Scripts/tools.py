import pygame

from .manager import icon_type_function
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, FONTS, COLOURS


class Timer():

    def __init__(self):
        self.counter = 0

    def time(self, timer, *events):
        self.counter += 1
        if self.counter > timer * 100:
            self.counter = 0
            return events


class Sprite_sheet(pygame.sprite.Sprite):

    def __init__(self, *args):
        super().__init__()
        self.sheet = pygame.image.load(*args).convert_alpha()
        self.animation_dict = {}
        self.update_time = pygame.time.get_ticks()
        self.action = 0
        self.frame_index = 0

    def get_image(self, width, height, frame_x, frame_y, scale):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame_x * width), (frame_y * height), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(False)

        return image

    def create_animation(self, width, height, *args, scale=1):
        # Autocomplete values from frame_dict
        frame_dict = args == () and {0: (1, 1, 1, 1)} or args[0]
        frame_dict[0] = (1, 1, 1, 1)
        counter_x = counter_y = 0

        for key, value in frame_dict.items():
            if type(value) is not tuple: value = [value]
            value = list(value)
            while len(value) < 4: value.append(0)

            else:
                temp_img_list = []

                # Place frame_x if indicated
                if value[2] != 0: counter_y = value[2] - 1
                for _y in range(value[1]):
                    counter_x = 0

                    # Place frame_y if indicated
                    if value[3] != 0: counter_x = value[3] - 1
                    for _x in range(value[0]):
                        temp_img_list.append(self.get_image(width, height, counter_x, counter_y, scale))
                        counter_x += 1
                    counter_y += 1

                self.animation_dict[key] = temp_img_list

        return self.animation_dict

    def update_animation(self, animation_cooldown=100, repeated_frame=0):
        # Update image depending on current frame
        self.image = self.animation_dict[self.action][self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks() # Current time
            self.frame_index += 1
        # If the animation has move out the reset back to the start
        if self.frame_index >= len(self.animation_dict[self.action]) - repeated_frame:
            if self.action == 'destroy':
                self.kill() # Kill the animation
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # Check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        # Draw player on screen
        self.screen.blit(self.image, self.rect)


class Canvas(pygame.sprite.Sprite):
    def __init__(self, **kwargs):
        super().__init__()
        self._text = ""
        self.kwargs = kwargs

        self.x = self._keys('x') or self.is_right() or 20
        self.y = self._keys('y') or 10
        self.letter_f = self._keys('letter_f') or FONTS[0]
        self.size = self._keys('size') or 28
        self.color = self._keys('color') or COLOURS('WHITE')

        self.font = pygame.font.Font(f"Assets/Fonts/{self.letter_f}.ttf", self.size)
        self.image = self.font.render(self._text, True, self.color)
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def update(self):
        self.image = self.font.render(self._text, True, self.color)
        self.rect = self.image.get_rect(x=self.x, y=self.y)
        self.is_right_text()
        self.is_right()
        self.is_center()

    def _keys(self, key):
        return key in self.kwargs.keys() and self.kwargs[key]

    def is_right_text(self):
        if self._keys('right_text'):
            self.x = SCREEN_WIDTH - (20 + len(self.text) * 12)

    def is_right(self):
        if self._keys('right'):
            self.x = SCREEN_WIDTH - (20 + len(self.text) * 15)

    def is_center(self):
        if self._keys('center'):
            self.x = SCREEN_WIDTH // 2 - self.rect.w // 2

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)


class Icon(Sprite_sheet):

    def __init__(self, screen, icon_type, **kwargs):
        icon_img, icon_type_dict = icon_type_function(icon_type)
        super().__init__(icon_img)
        self.screen = screen

        # Load icon image
        self.create_animation(100, 100, icon_type_dict)
        self.image = self.animation_dict[self.action][self.frame_index]
        # Get icon rect
        self.rect = self.image.get_rect(**kwargs)

    def update(self, select):
        # Update player events
        self.update_animation()
        self.icon_select(select)

    def icon_select(self, select):
        # Select icon type
        if select == 0:
            self.update_action('dps')
        if select == 1:
            self.update_action('tank')
        if select == 2:
            self.update_action('heal')
