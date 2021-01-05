from math import hypot, atan2, cos, sin

import pygame as pg

from config import Configuration as Conf
from utils.resources.image import Image as Img


class Sprite(pg.sprite.Sprite):
    """ A class Sprite

    The class is a wrap for pygame.sprite.Sprite.
    Adds usable attributes.

    Attributes
    ----------
    texture : pg.Surface
        immutable image of sprite, that can be used for wearing sprite
    image : pg.Surface
        mutable image of sprite, that shows on the screen
    """

    def __init__(self, texture: pg.Surface):
        super().__init__()
        self.texture: pg.Surface = texture
        self.image: pg.Surface = texture

    def set_texture(self, texture: pg.Surface) -> None:
        """
        Changes sprite's image.
        :param texture: new sprite's image
        """
        self.texture = texture
        self.image = texture


class TextureUpdatable(Sprite):
    """ An interface TextureUpdatable.

    Allows changing sprite's texture in the time of playing.

    Attributes
    ----------
     needs_update : bool
        flag contains if this type of sprite needs updating
    texture_num : int
        number of the texture from pack
    """

    needs_update: bool
    texture_num: int

    def update_texture(self, texture: pg.Surface) -> None:
        """
        Changes texture of the sprite if this type needs.
        :param texture: new sprite's texture
        """
        super().set_texture(texture)
        type(self).needs_update = False

    @classmethod
    def set_texture_num(cls, num: int) -> None:
        """
        Sets new number of the sprite type texture.
        :param num: number of the new texture
        """
        cls.texture_num = num
        cls.needs_update = True


class Locatable(Sprite):
    """ An interface Locatable

    Allows placing the sprite into the screen using <Sprite.object>.locate(x, y).

    Attributes
    ----------
     pos_x : float
        position of the left top angle of the sprite on x axis
    pos_y : float
        position of the left top angle of the sprite on y axis
    """
    def __init__(self, texture: pg.Surface):
        super().__init__(texture)
        self.pos_x: float = 0
        self.pos_y: float = 0

    def locate(self, x: float = None, y: float = None, **kwargs) -> None:
        """
        Places the sprite into the screen. Saves coordinates.
        :param x: coordinate on x axis
        :param y: coordinate on y axis
        :param kwargs: angle coordinates
        """
        if x is None or y is None:
            self.rect = self.image.get_rect(**kwargs)
        else:
            self.rect = self.image.get_rect(center=(x, y))
        self.pos_x = self.rect.centerx
        self.pos_y = self.rect.centery


class Transparent(Locatable):
    """ An interface Transparent

    Makes implemented sprite transparent.

    Attributes
    ----------
    opacity : int
        0 <= opacity <= 100
        default: 100
        percentage of the transparency
    """
    def __init__(self, texture: pg.Surface, opacity: int = 100):
        texture.set_alpha(opacity)
        super().__init__(texture)
        self.opacity = opacity

    def set_opacity(self, opacity: int) -> None:
        """
        Changes percentage of the transparency.
        :param opacity : new opacity value
         """
        self.opacity = opacity
        self.texture.set_alpha(opacity)

    def get_opacity(self) -> int:
        """
        Returns opacity value.
        :return: percentage of the transparency
        """
        return self.opacity

    def set_texture(self, texture: pg.Surface) -> None:
        """
        Overriding Sprite.set_texture(texture) with saving opacity.
        :param texture: new sprite's image
        """
        texture.set_alpha(self.opacity)
        super().set_texture(texture)


class Text(Locatable):
    """ An class Text

    Creates sprite to show text.

    Attributes
    ----------
    font : pg.font.Font
        font for rendering the text
    color : color of the text
    value :
    """
    def __init__(self, font: pg.font.Font, color: tuple[int, int, int], value: object = ""):
        super().__init__(
            texture=font.render(str(value), True, color)
        )
        self.font: pg.font.Font = font
        self.color: tuple[int, int, int] = color
        self.value: str = str(value)
        self._args: dict = {}

    def locate(self, x: float = None, y: float = None, **kwargs) -> None:
        """
        Overriding Locatable.locate(x, y, **kwargs) with saving arguments.

        Places the sprite into the screen. Saves coordinates.
        :param x: coordinate on x axis
        :param y: coordinate on y axis
        :param kwargs: angle coordinates
        """
        super().locate()
        self._args = dict(x=x, y=y, **kwargs)

    def set_value(self, value: object) -> None:
        """
        Changes showing text. Receiving object, parsing into <str.object>, shows.
        :param value: new showing text
        """
        self.value = str(value)
        super().set_texture(self.font.render(self.value, True, self.color))
        super().locate(**self._args)

    def get_value(self) -> str:
        """
        Returns showing text as <str.object>.
        :return: showing text
        """
        return self.value


class Movable(Locatable):
    """ An interface Movable

    Allows moving sprite via setting x and y speed, calling <Movable.object>.move()
    every frame.

    Attributes
    ----------
    speed_x : float
        x move distance per one frame
    speed_y : float
        y move distance per one frame
    """
    def __init__(self, texture: pg.Surface, speed_x: float = 0, speed_y: float = 0):
        super().__init__(texture)
        self.speed_x: float = speed_x
        self.speed_y: float = speed_y

    def set_speed(self, speed_x: float, speed_y: float) -> None:
        """
        Changes speed.
        :param speed_x: new x axis speed
        :param speed_y: new y axis speed
        """
        self.speed_x = speed_x
        self.speed_y = speed_y

    def get_speed(self) -> tuple[float, float]:
        """
        Returns speed
        :return: x and y speed
        """
        return self.speed_x, self.speed_y

    def move(self) -> None:
        """ Moves the sprite consider FPS. """
        self.pos_x += self.speed_x * Conf.System.SCALE
        self.pos_y += self.speed_y * Conf.System.SCALE
        self.rect.centerx = round(self.pos_x)
        self.rect.centery = round(self.pos_y)


class Rotatable(Movable):
    """ An interface Rotatable

    Allows rotating sprite, using <Rotatable.object>.rotate(delta_angle, rotator)

    Attributes
    ----------
    angle : float
        angle of rotating at the moment
    rotator : callable(float)
        function, getting rotate angle and returning texture for this angle
    """
    def __init__(self, texture: pg.Surface, speed_x: float = 0, speed_y: float = 0, rotator: callable(float) = None):
        super().__init__(texture, speed_x, speed_y)
        self.angle: float = 0
        self.rotator: callable(float)
        if rotator is None:
            self.rotator = lambda deg: pg.transform.rotate(self.texture, deg)
        else:
            self.rotator = rotator

    def rotate(self, delta_angle: float = 0) -> None:
        """
        Rotates the sprite with possibility of using another realisation of the rotator.
        :param delta_angle: difference between the last angle and the new angle
        """
        x_offset = self.pos_x - self.rect.centerx
        y_offset = self.pos_y - self.rect.centery
        self.angle = (self.angle + delta_angle * Conf.System.SCALE) % 360
        self.image = self.rotator(self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.pos_x = self.rect.centerx + x_offset
        self.pos_y = self.rect.centery + y_offset


class Acceleratable(Movable):
    """ An interface Acceleratable

    Allows moving sprite consider to Physics.
    Use <Acceleratable.object>.accelerate(x, y, weight, power, resist) to
    give axel to sprite and to change axes speed.

    Attributes
    ----------
    weight : float
        abstract of the sprite
    power : float
        power of the sprite
    resist : float
        abstract resisting multiplier of the environment
    """

    def __init__(self, texture: pg.Surface, weight: float, power: float, resist: float):
        super().__init__(texture)
        self.weight = weight
        self.power = power
        self.resist = resist

    def accelerate(self, x: float, y: float):
        """
        Changes axis speed, from axel vector
        :param x: coordinate of the axel vector -1 <= x <= 1
        :param y: coordinate of the axel vector -1 <= y <= 1
        """
        assert -1 <= x <= 1 and -1 <= y <= 1
        a = Acceleratable.PhysCalc.axel(x, y, self.power)
        r = Acceleratable.PhysCalc.resist(self.speed_x, self.speed_y, self.resist)
        self.speed_x += (a[0] - r[0]) / self.weight
        self.speed_y += (a[1] - r[1]) / self.weight

    class PhysCalc:
        """ A static class for calculating physics metrics:
        for axel: PhysCalc.axel(x, y, power),
        for resist: PhysCalc.resist(speed_x, speed_y, resist)
        """
        @staticmethod
        def axel(x: float, y: float, power: float) -> tuple[float, float]:
            """
            Calculates axel by the vector coordinates
            :param x: vector coordinate
            :param y: vector coordinate
            :param power: strength
            :return: axel vector
            """
            force = min(1.0, hypot(x, y))
            rad = atan2(y, x)
            a_x = power * cos(rad) * force
            a_y = power * sin(rad) * force
            return a_x, a_y

        @staticmethod
        def resist(speed_x: float, speed_y: float, resist: float) -> tuple[float, float]:
            """
            Calculates resisting by the vector coordinates
            :param speed_x: sprite's speed on x axis
            :param speed_y: sprite's speed on y axis
            :param resist: resisting multiplier
            :return: resisting vector
            """
            speed = hypot(speed_x, speed_y)
            rad = atan2(speed_y, speed_x)
            r = resist * pow(speed, 2)
            r_x = r * cos(rad)
            r_y = r * sin(rad)
            return r_x, r_y


class AcceleratableWithFire(Acceleratable):
    """ An interface AcceleratableWithFire

    Wrap for the Acceleratable with possibility of changing
    textures when it has power and it doesn't.

    Attributes
    ----------
    texture_pack : tuple[pg.Surface, pg.Surface]
        tuple of textures: normal and with fire
    with_fire : bool
        flag, if fire texture is turned on
    """
    def __init__(self, texture_pack: tuple[pg.Surface, pg.Surface], weight: float, power: float, resist: float):
        super().__init__(texture_pack[0], weight, power, resist)
        self.texture_pack: tuple[pg.Surface, pg.Surface] = texture_pack
        self.with_fire: bool = False

    def accelerate(self, x: float, y: float) -> None:
        """
        Wrap for the <Acceleratable.object>.accelerate(x, y), changing textures

        Changes axis speed, from axel vector
        :param x: coordinate of the axel vector -1 <= x <= 1
        :param y: coordinate of the axel vector -1 <= y <= 1
        """
        self.wear_fire((x, y) != (0, 0))
        super().accelerate(x, y)

    def wear_fire(self, with_fire: bool) -> None:
        """
        Changes textures consider to with_fire
        :param with_fire: True if fire texture should be turned on
        """
        if with_fire != self.with_fire:
            self.with_fire = with_fire
            self.texture = self.texture_pack[1] if with_fire else self.texture_pack[0]
            if isinstance(self, Rotatable):
                self.rotate()
            else:
                self.image = self.texture
            self.rect = self.image.get_rect(center=self.rect.center)

    def set_texture(self, texture_pack: tuple[pg.Surface, pg.Surface]) -> None:
        """
        Overriding <Sprite.object>.set_texture(texture), receiving tuple of textures
        :param texture_pack: new textures for 2 states
        """
        self.texture_pack = texture_pack


class Group(pg.sprite.Group):
    """ A class Group

    Wrapper for pg.sprite.Group with possibility of killing all sprites
    in the group using <Group.object>.kill()
    """
    def kill(self) -> None:
        """ Kills anyone sprite in the group """
        for sprite in self:
            sprite.kill()
        super().empty()
