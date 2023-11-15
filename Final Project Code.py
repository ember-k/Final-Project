from dataclasses import dataclass
from designer import *
from random import randint

"""
# Phase 2
- [ ] Fish move: fish move left and right across the screen while moving generally downwards
- [ ] fish wrap: if fish move down to the bottom of the screen, they wrap back to the top
- [ ] Screen limits: fish can't move off screen
- [ ] fish collision: When the hook touches a fish, points are gained and the type & number of fish collisions are recorded.
- [ ] Max collisions: Only a certain number of fish can be caught before the hook is full
"""

HOOK_SPEED = 10
FISH_SPEED = 5
DOWN_SPEED = 5
@dataclass
class Screen:
    background: DesignerObject # Rectangle
    elements: list[DesignerObject] #text


@dataclass
class World:
    start: bool
    aquatic_background: Screen
    hook: DesignerObject
    fish: list[DesignerObject]
    start_page: Screen
    hook_move_left: bool
    hook_move_right: bool
    hook_speed: int
    #fish_speed: int



def create_world() -> World:
    """
    Creates the world with all necessary attributes of the World dataclass
    :return World: the game's world instance
    """
    return World(False, create_background(), create_hook(), [], create_start_page(), False, False, HOOK_SPEED)#, FISH_SPEED) #create_fish()

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
    print(get_width())
    print(get_height())
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
        world.start = True
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
    print(hook.y)
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
"""
def create_fish() -> DesignerObject:
    ""
    Spawns 4 fish at random positions on the right and left sides of the window (8 fish total)
    :return DesignerObject: a list of 8 fish
    ""
    fish = []
    for index, a_fish in enumerate(range(8)):
        a_fish = emoji("fish") #tropical
        a_fish.scale = 1.5
        if index < 4:
            a_fish.y = randint(0, 20) + 100 * index
            a_fish.x = randint(0, get_width() // 9) + (index * 2)
            a_fish.flip_x = True
        else:
            a_fish.y = randint(0, 20) + 100 * (8-index)
            a_fish.x = randint(get_width() - get_width() // 9, get_width())
        fish.append(a_fish)
    return fish
"""
def create_fish() -> DesignerObject:
    a_fish = emoji("tropical fish")
    a_fish.anchor = 'midbottom'
    a_fish.scale = 1.5
    a_fish.y = randint(0, 25) * 12
    if randint(1, 2) == 2:
        a_fish.x = 0
        a_fish.flip_x = True
    else:
        a_fish.x = get_width()
    return a_fish
"""
def make_fires(world: World):
    not_too_many_fires = len(world.fires) <= 10
    random_chance = randint(1, 100) == 1
    if not_too_many_fires and random_chance:
        world.fires.append(create_fire())
"""
def spawn_fish(world: World):
    """ Create a new fish at random times, if there aren't enough fish """
    not_too_many_fish = len(world.fish) < 10
    random_chance = randint(1, 20) == 1
    if not_too_many_fish and random_chance:
        world.fish.append(create_fish())
    return

def move_fish(world: World):
    # direction matters (if it's flipped)
    for fish in world.fish:
        if fish.flip_x:
            fish.x += FISH_SPEED
        else:
            fish.x -= FISH_SPEED
    return


def bounce_fish(world: World):
    for fish in world.fish:
        if fish.x > get_width():
            fish.flip_x = False
        elif fish.x < 0:
            fish.flip_x = True
    return

def make_fish_fall(world: World):
    if (world.start):
        for fish in world.fish:
            fish.y += DOWN_SPEED
        for element in world.aquatic_background.elements:
            element.y += DOWN_SPEED
    return

def wrap_fish(world: World):
    for fish in world.fish:
        if fish.y > get_height() + 10:
            fish.y = 0
    return


def start_animation(world: World):
    if world.start:
        move_fish(world)
        bounce_fish(world)
        make_fish_fall(world)
        wrap_fish(world)
        spawn_fish(world)
    return

when('starting', create_world)
when('typing', hide_start_page)
when('typing', keys_down)
when('done typing', keys_realeased)
when('updating', set_direction)
when("updating", start_animation)
#when("updating", move_fish)
#when("updating", bounce_fish)
#when("updating", make_fish_fall)
start()
