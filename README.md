<h1 align="center">
    Mini-Games
</h1>

<h3 align="center"> |
    <a href="#Description"> Description </a> |
    <a href="#Getting-Started"> Getting Started </a> |
    <a href="#Built-With"> Built With </a> |
    <a href="#Authors"> Authors </a> |
    <a href="#License"> License </a> |
</h3> 

## Description

Pack of mini-games on Python

Includes:
**1. Space Battle**

Game with flying _asteroids_. You play as a _spaceship_, shooting _rockets_.

**Control**

* _Keyboard_
    * W, A, S, D, arrow keys - move
    * Mouse - rotate
    * Left Mouse Button - shoot
    * Esc - pause
    * Space + Enter - self-destruction
    
* _Gamepad_
    * LS - move
    * RS - rotate
    * RT - shoot
    * Start - pause
    * LS click + RS click - self-destruction
        
**2. Tetris**

Analog of the classic Tetris game. Your goal is to build full horizontal line.

**Control**

* _Keyboard_ | _Gamepad_
    * UP | DPad UP - rotate
    * DOWN | DPad DOWN - step passing
    * LEFT, RIGHT | DPad LEFT \ RIGHT - move to side

**3. Crosses**

Classic Crosses game.

**Opponent**
* Player
* Bot

## Getting Started

### Easy way

1. Download archive from **releases**
2. In the archive start _<game_name>.exe_

### Using source files
1. Install [Python](https://www.python.org/)
2. Install all [requirements](#Requirements) via the commands from [Installing](#Installing)
3. Run **main.py** from <game_name>


### Requirements

* Python 3.8
    * Tkinter

#### For the Space Battle

* PyGame
* PyGame-menu


### Installing

#### First
```
pip install pip
pip install --upgrade pip
```
#### For the SpaceBattle
```
pip install pygame
pip install pygame_menu
```


## Built With

* [Python 3.9](https://www.python.org) - Language
* [Tkinter](https://tkdocs.com) - GUI framework + event handler
* [PyGame](https://www.pygame.org/news) - GUI framework + event handler
* [PyGame-menu](https://pygame-menu.readthedocs.io/en/latest/) - PyGame's library for creating menu


## Author

* [**Derbin Dmitriy**](https://github.com/T1GIT) - controls, ship, project structure, many improvements
* [**Bakanov Artem**](https://github.com/Attilene) - meteors, rockets, colliding, game
* [**Kurtaev Damir**](https://github.com/Amikuto) - menu, sound


## License

This project is licensed under the GPL v3.0 License - see the [LICENSE](LICENSE) file for details


### Version 1.2
#### 18.12.2020
