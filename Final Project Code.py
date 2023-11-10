from dataclasses import dataclass
from designer import *
from random import randint
HOOK_SPEED = 10

@dataclass
class Screen:
    background: DesignerObject # Rectangle
    elements: list[DesignerObject] #text


@dataclass
class World:
    aquatic_background: Screen
    hook: DesignerObject
    fish: list[DesignerObject]
    start_page: Screen
    hook_move_left: bool
    hook_move_right: bool
    hook_speed: int



def create_world() -> World:
    """Create the world"""
    return World(create_background(), create_hook(), create_fish(), create_start_page(), False, False, HOOK_SPEED)

def create_start_page() -> DesignerObject:
    start_page = Screen(rectangle("yellow", get_width() * 0.8, get_height() * 0.8),
                        [text("black", "FISHING GAME", 45, None, get_height() * (1/3), "midbottom", Text.DEFAULT_FONT_NAME),
                        emoji("tropical fish"),
                        text("black", "Press the space bar to play", 15, None, get_height() * (2/3), "midtop", Text.DEFAULT_FONT_NAME)])
    return start_page

def hide_start_page(world: World, key: str):
    if key == "space":
        world.start_page.background.visible = False
        for element in world.start_page.elements:
            element.visible = False
    return

def create_background() -> DesignerObject:
    """Create the aquatic background"""
    aquatic_background = Screen(rectangle("deepskyblue", get_width(), get_height()),
                                [image("https://clipart-library.com/images_k/seaweed-transparent-background/seaweed-transparent-background-2.png", get_width() * 0.8, get_height() + 20),
                                image("https://clipart-library.com/images_k/seaweed-transparent-background/seaweed-transparent-background-2.png", get_width() - get_width() * 0.82, get_height() + 20)])
    return aquatic_background


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
    """Create the fish at the two sides of the window"""
    fish = []
    for index, a_fish in enumerate(range(8)):
        a_fish = emoji("tropical fish")
        a_fish.scale = 1.5
        if index < 4:
            a_fish.y = randint(0, 20) + 80 * index
            a_fish.x = randint(0, get_width() // 9)
            a_fish.flip_x = True
        else:
            a_fish.y = randint(0, 20) + 80 * (8-index) #a_fish.y = randint(40 * (6-index), 40 * ((6-index) + 1)) + 20
            a_fish.x = randint(get_width() - get_width() // 9, get_width())
        fish.append(a_fish)
    return fish




when('starting', create_world)
when('typing', hide_start_page)
when('typing', keys_down)
when('done typing', keys_realeased)
when('updating', set_direction)
start()
