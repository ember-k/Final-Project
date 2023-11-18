from dataclasses import dataclass
from designer import *
from random import randint

"""
# Phase 2
- [x] Fish move: fish move left and right across the screen while moving generally downwards
- [x] fish wrap: if fish move down to the bottom of the screen, they wrap back to the top
- [x] Screen limits: fish can't move off screen
- [ ] fish collision: When the hook touches a fish, points are gained and the type & number of fish collisions are recorded.
- [ ] Max collisions: Only a certain number of fish can be caught before the hook is full -> CHANGE TO A TIMER SYSTEM
"""

HOOK_SPEED = 10
FISH_SPEED = 10
DOWN_SPEED = 5
POINTS_PER_FISH = 1
FISH_CAUGHT_CAP = 10
FISH_SPAWN_CAP = 7
TIMER = 500
@dataclass
class Screen:
    background: DesignerObject # Rectangle
    elements: list[DesignerObject] #text, images, etc.



@dataclass
class World:
    play: bool
    catch_zone: DesignerObject
    aquatic_background: Screen
    hook: DesignerObject
    fish: list[DesignerObject]
    start_page: Screen
    hook_move_left: bool
    hook_move_right: bool
    hook_speed: int
    score: int
    time: int




def create_world() -> World:
    """
    Creates the world with all necessary attributes of the World dataclass
    :return World: the game's world instance
    """
    return World(False, create_catch_zone(), create_background(), create_hook(), [], create_start_page(), False, False,
                 HOOK_SPEED, 0, TIMER)

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
        world.play = True
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

def create_catch_zone() -> DesignerObject:
    """Creates the zone on the hook where fish collide and are caught (width and height are arbitrary)"""
    return rectangle("deepskyblue", 10, 10)

def adjust_catch_zone(world: World):
    """
    Sets the width and height of the catch zone and moves the catch zone in relation to the hook as the game updates
    :param world: the game's world instance
    """
    world.catch_zone.x = world.hook.x - 20
    world.catch_zone.y = world.hook.y + world.hook.height * (3/4)
    world.catch_zone.width = world.hook.width // 3
    world.catch_zone.height = world.hook.height // 4
    return

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

def set_hook_direction(world: World):
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
    Creates a fish with a given size and a random position on either the right or left side of the screen
    :return a_fish: a fish designer object
    """
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

def spawn_fish(world: World):
    """
    Spawn a new fish at a random time if there aren't enough fish on the screen
    :param world: the game's world instance
    """
    not_too_many_fish = len(world.fish) < FISH_SPAWN_CAP
    random_chance = randint(1, 20) == 1
    if not_too_many_fish and random_chance:
        world.fish.append(create_fish())
    return

def move_fish_horizontally(world: World):
    """
    Moves the fish either right or left depending on which way they're facing
    :param world: the game's world instance
    """
    for fish in world.fish:
        if fish.flip_x:
            fish.x += FISH_SPEED
        else:
            fish.x -= FISH_SPEED
    return


def bounce_fish(world: World):
    """
    Prevents the fish from moving beyond the left or right wall of the window by flipping them around
    :param world: the game's world instance
    """
    for fish in world.fish:
        if fish.x > get_width():
            fish.flip_x = False
        elif fish.x < 0:
            fish.flip_x = True
    return

def make_fish_fall(world: World):
    """
    Moves the fish and seaweed downward across the screen
    :param world: the game's world instance
    """
    for fish in world.fish:
        fish.y += DOWN_SPEED
    for element in world.aquatic_background.elements:
        element.y += DOWN_SPEED
    return

def wrap_fish(world: World):
    """
    Fish wrap around to the top of the screen when they've passed the bottom edge of the window
    :param world: the game's world instance
    """
    for fish in world.fish:
        if fish.y > get_height() + 10:
            fish.y = 0
    return

def track_time(world: World):
    """
    Stops gameplay when the timer has counted down to 0
    :param world: the game's world instance
    """
    world.time -= 1
    if world.time <= 0:
        world.play = False
    return

def start_animation(world: World):
    """
    When the gameplay condition is true, start_animation calls functions related to fish creation & movement,
    hook & catch zone movement, and the timer countdown.
    :param world: the game's world instance
    """
    if world.play:
        set_hook_direction(world)
        move_fish_horizontally(world)
        bounce_fish(world)
        make_fish_fall(world)
        wrap_fish(world)
        spawn_fish(world)
        adjust_catch_zone(world)
        track_time(world)
    return

def fish_caught_by_hook(world: World):
    """
    Increases score when a fish collides with the hook's catch zone and calls a function to destroy caught fish
    :param world: the game's world instance
    """
    caught_fish = []
    for fish in world.fish:
        if colliding(fish, world.catch_zone):
            caught_fish.append(fish)
            world.score += POINTS_PER_FISH
            print(world.score)
    world.fish = destroy_caught_fish(world.fish, caught_fish)
    return

def destroy_caught_fish(all_fish: list[DesignerObject], caught_fish: list[DesignerObject]) -> list[DesignerObject]:
    """
    Helper function that destroys fish that have been caught by the hook
    :param all_fish: the original list of fish (both caught fish and free fish)
    :param caught_fish: a list of fish that have been caught by the hook
    :return remaining fish: returns only the fish that haven't been caught
    """
    remaining_fish = []
    for item in all_fish:
        if item in caught_fish:
            destroy(item)
        else:
            remaining_fish.append(item)
    return remaining_fish


when('starting', create_world)
when('typing', hide_start_page)
when('typing', keys_down)
when('done typing', keys_realeased)
when("updating", start_animation)
when("updating", fish_caught_by_hook)
start()
