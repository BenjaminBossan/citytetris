from typing import Protocol

import pygame


DARKGRAY = pygame.Color(70, 70, 70)


class ColorShade(Protocol):
    fill: pygame.Color
    light: pygame.Color
    dark: pygame.Color


class GrayShade:
    def __init__(self) -> None:
        self.fill = pygame.Color(128, 128, 128)
        self.light = pygame.Color(200, 200, 200)
        self.dark = pygame.Color(25, 25, 25)


class RedShade:
    def __init__(self) -> None:
        self.fill = pygame.Color(170, 25, 25)
        self.light = pygame.Color(255, 50, 50)
        self.dark = pygame.Color(150, 0, 0)


class GreenShade:
    def __init__(self) -> None:
        self.fill = pygame.Color(25, 170, 25)
        self.light = pygame.Color(50, 255, 50)
        self.dark = pygame.Color(0, 150, 0)


class BlueShade:
    def __init__(self) -> None:
        self.fill = pygame.Color(50, 50, 220)
        self.light = pygame.Color(80, 80, 255)
        self.dark = pygame.Color(0, 0, 150)


class YellowShade:
    def __init__(self) -> None:
        self.fill = pygame.Color(180, 180, 25)
        self.light = pygame.Color(255, 255, 50)
        self.dark = pygame.Color(150, 150, 0)


class CyanShade:
    def __init__(self) -> None:
        self.fill = pygame.Color(25, 200, 200)
        self.light = pygame.Color(50, 255, 255)
        self.dark = pygame.Color(0, 150, 150)


class PurpleShade:
    def __init__(self) -> None:
        self.fill = pygame.Color(180, 50, 180)
        self.light = pygame.Color(255, 50, 255)
        self.dark = pygame.Color(150, 0, 150)


class OrangeShade:
    def __init__(self) -> None:
        self.fill = pygame.Color(200, 150, 25)
        self.light = pygame.Color(255, 200, 50)
        self.dark = pygame.Color(150, 100, 0)
