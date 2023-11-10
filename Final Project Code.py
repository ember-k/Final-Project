from dataclasses import dataclass
from designer import *
from random import randint
HOOK_SPEED = 10

"""
- [ ] Setting: Program the aquatic background
- [x] Hook exists: the hook exists on the screen and remains vertically centered for the duration of the game.
- [ ] Hook movement: The player can use the arrow keys to move the hook left and right (i might try to get dragging to work as a bonus in phase 3)
- [x] Screen limits: the hook can't be moved off screen (the hook can't move further once it hits the side)
- [ ] Fish exist: Fish appear from either side of the screen
"""
# https://images.emojiterra.com/openmoji/v13.1/512px/1fa9d.png

@dataclass
class World:
    water: DesignerObject
    hook: DesignerObject
    fish: list[DesignerObject]
    start_page: DesignerObject
    hook_move_left: bool
    hook_move_right: bool
    hook_speed: int



def create_world() -> World:
    """Create the world"""
    return World(create_background(), create_hook(), create_fish(), create_start_page(), False, False, HOOK_SPEED)

def create_start_page() -> DesignerObject:
    start_page = rectangle("yellow", get_width() * 0.8, get_height() * 0.8)
    start_page.anchor = 'center'
    text("black", "FISHING GAME", 15, None, None, "center")
    return start_page

def hide_start_page(world: World, key: str):
    if key == "space":
        world.start_page.visible = False

def create_background() -> DesignerObject:
    """Create the water"""
    water = rectangle("deepskyblue", get_width(), get_height())
    return water


def create_hook() -> DesignerObject:
    """Create the hook"""
    hook = image("https://images.emojiterra.com/openmoji/v13.1/512px/1fa9d.png")
    shrink(hook, 3)
    hook.anchor = "midtop"
    return hook

def move_hook(world: World, direction: int):
    """Move the hook horizontally"""
    world.hook.x += world.hook_speed * direction

def hook_at_left_edge(world: World):
    """Prevents the hook from moving beyond the left wall of the window"""
    if world.hook.x < world.hook.width / 2.9:
        world.hook_move_left = False
        return True
    else:
        return False
def hook_at_right_edge(world: World):
    """Prevents the hook from moving beyond the right wall of the window"""
    if world.hook.x > get_width() - world.hook.width / 4.5:
        world.hook_move_right = False
        return True
    else:
        return False

def set_direction(world: World):
    """Change direction of hook path according to arrow keys"""
    if world.hook_move_left and (not hook_at_left_edge(world)):
        move_hook(world, -1)
    elif world.hook_move_right and (not hook_at_right_edge(world)):
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

def create_fish() -> DesignerObject:
    """Create the fish"""
    fish = []
    for index, a_fish in enumerate(range(6)):
        a_fish = emoji("tropical fish")
        a_fish.scale = 1.5
        a_fish.y = randint(0, get_height() * (1/3)) + 10
        if index < 3:
            a_fish.x = randint(0, get_width() / 10)
            a_fish.flip_x = True
        else:
            a_fish.x = randint(get_width() // 1.2, get_width())
        fish.append(a_fish)
    return fish




when('starting', create_world)
when('typing', hide_start_page)
when('typing', keys_down)
when('done typing', keys_realeased)
when('updating', set_direction)
start()
