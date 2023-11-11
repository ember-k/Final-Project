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
    """
    Creates the world with all necessary attributes of the World dataclass
    :return World: the game's world instance
    """
    return World(create_background(), create_hook(), create_fish(), create_start_page(), False, False, HOOK_SPEED)

def create_start_page() -> DesignerObject:
    """
    Creates the start screen displaying the game's title and the player's current score
    :return DesignerObject: the start page
    """
    start_page = Screen(rectangle("yellow", get_width() * 0.8, get_height() * 0.8),
                        [text("black", "THE FISHING GAME", 45, None, get_height() * (1/3),
                              "midbottom", "ComicSans"),
                         text("black", "Score: ____ ", 25, None, get_height() * (2 / 3),
                              "midbottom","ComicSans"),
                         emoji("fish"),
                         text("black", "Press the space bar to play", 15, None,
                              get_height() * (3/4), "midtop", "CopperPlate")])
    return start_page

def hide_start_page(world: World, key: str):
    """
    Hides the starting screen's components when the space button is pressed
    :param world: the game's world instance
    :param key: the key that was pressed
    """
    if key == "space":
        world.start_page.background.visible = False
        for element in world.start_page.elements:
            element.visible = False
    return

def create_background() -> DesignerObject:
    """Creates and returns the aquatic background with water and kelp"""
    aquatic_background = Screen(rectangle("deepskyblue", get_width(), get_height()),
                                [image("https://clipart-library.com/images_k/seaweed-transparent-background/seaweed-transparent-background-2.png",
                                       get_width() * 0.8, get_height() + 20),
                                image("https://clipart-library.com/images_k/seaweed-transparent-background/seaweed-transparent-background-2.png",
                                      get_width() - get_width() * 0.82, get_height() + 20)])
    return aquatic_background


def create_hook() -> DesignerObject:
    """Creates and returns the hook"""
    hook = image("https://images.emojiterra.com/openmoji/v13.1/512px/1fa9d.png")
    shrink(hook, 3)
    hook.anchor = "midtop"
    return hook

def move_hook(world: World, direction: int):
    """
    Moves the hook horizontally
    :param world: the game's world instance
    :param direction: either -1, 0, or 1 indicating left-, no movement, or right-facing movement
    """
    world.hook.x += world.hook_speed * direction
    return

def hook_at_left_edge(world: World):
    """
    Prevents the hook from moving beyond the left wall of the window
    :param world: the game's world instance
    :return bool: returns true if the hook is nearly touching the left wall of the window; returns false otherwise.
    """
    if world.hook.x < world.hook.width / 2.9:
        world.hook_move_left = False
        return True
    else:
        return False

def hook_at_right_edge(world: World):
    """
    Prevents the hook from moving beyond the right wall of the window
    Returns: returns true if the hook is nearly touching the right wall of the window; returns false otherwise.
    :param world: the game's world instance
    """
    if world.hook.x > get_width() - world.hook.width / 4.5:
        world.hook_move_right = False
        return True
    else:
        return False

def set_direction(world: World):
    """
    Determines the direction of hook path according to arrow key input and whether the function is at a window boundary,
    then it moves the hook accordingly by calling the move_hook function.
    :param world: the game's world instance
    """
    if world.hook_move_left and (not hook_at_left_edge(world)):
        move_hook(world, -1)
    elif world.hook_move_right and (not hook_at_right_edge(world)):
        move_hook(world, 1)
    else:
        move_hook(world, 0)
    return


def keys_down(world: World, key: str):
    """
    When a right or left arrow key is pressed, the respective boolean variable that determines if the hook should move
    right or left is set to true
    :param world: the game's world instance
    :param key: the key that was pressed
    """
    if key == "left":
        world.hook_move_left = True
    elif key == 'right':
        world.hook_move_right = True
    return

def keys_realeased(world: World, key: str):
    """
        When a right or left arrow key is released, the respective boolean variable that determines if the hook should
        move right or left is set to false
        :param world: the game's world instance
        :param key: the key that was pressed
        """
    if key == "left":
        world.hook_move_left = False
    elif key == 'right':
        world.hook_move_right = False
    return

def create_fish() -> DesignerObject:
    """
    Spawns 4 fish at random positions on the right and left sides of the window (8 fish total)
    :return DesignerObject: a list of 8 fish
    """
    fish = []
    for index, a_fish in enumerate(range(8)):
        a_fish = emoji("tropical fish")
        a_fish.scale = 1.5
        if index < 4:
            a_fish.y = randint(0, 20) + 80 * index
            a_fish.x = randint(0, get_width() // 9)
            a_fish.flip_x = True
        else:
            a_fish.y = randint(0, 20) + 80 * (8-index)
            a_fish.x = randint(get_width() - get_width() // 9, get_width())
        fish.append(a_fish)
    return fish




when('starting', create_world)
when('typing', hide_start_page)
when('typing', keys_down)
when('done typing', keys_realeased)
when('updating', set_direction)
start()
