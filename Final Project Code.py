from dataclasses import dataclass
from designer import *
from random import randint
HOOK_SPEED = 10

"""
- [ ] Play screen: the opening window with a high score counter and a play button
- [ ] Setting: Program the aquatic background
- [x] Hook exists: it exists on the screen
  of the screen and remain vertically centered for the remainder of the game.
- [ ] Hook movement: The player can drag the hook left and right
- [ ] Screen limits: the hook can't be moved off screen (the hook can't move further once it hits the side)
- [ ] Fish exist: Fish appear from either side of the screen
"""
# https://images.emojiterra.com/openmoji/v13.1/512px/1fa9d.png

@dataclass
class World:
    hook: DesignerObject
    water: DesignerObject
    hook_move_left: bool
    hook_move_right: bool
    hook_speed: int

def create_world() -> World:
    """Create the world"""
    return World(create_background(), create_hook(), False, False, HOOK_SPEED)
def create_background() -> DesignerObject:
    """Create the hook"""
    water = rectangle("cornflowerblue", get_window_width(), get_window_height())
    return water

def create_hook() -> DesignerObject:
    """Create the hook"""
    hook = image("https://images.emojiterra.com/openmoji/v13.1/512px/1fa9d.png", get_height() * (1/3), get_width() * (1/3))
    hook.flip_x = True
    return hook

def move_hook(world: World, direction: int):
    """Move the hook horizontally"""
    world.hook.x += world.hook_speed * direction

def set_direction(world: World):
    """Change direction of hook path according to arrow keys"""
    if world.hook_move_left:
        move_hook(world, -1)
    elif world.hook_move_right:
        move_hook(world, 1)
    else:
        move_hook(world, 0)

def keys_down(world:World, key:str):
    if key == "left":
        world.hook_move_left = True
    elif key == 'right':
        world.hook_move_right = True


def keys_realeased(world:World, key:str):
    if key == "left":
        world.hook_move_left = False
    elif key == 'right':
        world.hook_move_right = False



when('starting', create_background)
when('starting', create_world)
when('typing', keys_down)
when('done typing', keys_realeased)
when('updating', set_direction)
start()
