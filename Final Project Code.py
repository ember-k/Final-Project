from dataclasses import dataclass
from designer import *
from random import randint


HOOK_SPEED = 11
FISH_SPEED = 11
DOWN_SPEED = 4
POINTS_PER_FISH = 20
FISH_CAUGHT_CAP = 10
FISH_SPAWN_CAP = 8
TIMER = 500
SCENE_DELAY = 60


@dataclass
class Button:
    background: DesignerObject
    border: DesignerObject
    label: DesignerObject


def make_button(message: str, x: int, y: int) -> Button:
    """
    Creates a blue button with text
    :param message: The button's message
    :param x: the button's x-coordinate position
    :param y: the button's y-coordinate position
    :return: the button
    """
    horizontal_padding = 10
    vertical_padding = 8
    label = text("black", message, 20, x, y, layer='top')
    label.font = "CopperPlate"
    return Button(rectangle("deepskyblue",label.width + horizontal_padding,label.height + vertical_padding, x, y),
                  rectangle("black", label.width + horizontal_padding, label.height + vertical_padding, x, y,
                            1), label)


@dataclass
class TitleScreen:
    background: list[DesignerObject]
    header: DesignerObject
    fish: DesignerObject
    start_button: Button
    quit_button: Button


@dataclass
class ScoreScreen:
    background: list[DesignerObject]
    fish_count_message: DesignerObject
    fish_emoji: DesignerObject
    high_score_message: DesignerObject
    start_button: Button
    quit_button: Button
    high_score: int


@dataclass
class GameScreen:
    catch_zone: DesignerObject
    aquatic_background: list[DesignerObject]
    play: bool
    hook: DesignerObject
    fish: list[DesignerObject]
    caught_fish: list[DesignerObject]
    hook_move_left: bool
    hook_move_right: bool
    hook_speed: int
    high_score: int
    caught_fish_num: int
    time: int
    sky_elements: list[DesignerObject]
    scene_delay: int


def create_title_screen() -> TitleScreen:
    """
    Creates the start screen displaying the game's title and start & quit buttons
    :return DesignerObject: the start page
    """
    return TitleScreen([rectangle("deepskyblue", get_width(), get_height()), rectangle("yellow", get_width()
                                                                                       * 0.8, get_height() * 0.8)],
                       text("black", "THE FISHING GAME", 45, None, get_height() * (1/3),
                              "midbottom", "ComicSans"),
                       emoji("fish"),
                       make_button('Start', int(get_width() * 1/3), int(get_height() * 3/4)),
                       make_button('Quit', int(get_width() * 2/3), int(get_height() * 3/4)))


def create_game_screen(high_score: int) -> GameScreen:
    """
    Creates the game screen in which gameplay (including hook and fish movement) occurs
    :return DesignerObject: the game page
    """
    hook_catch_zone = create_catch_zone()
    hook_catch_zone.visible = False
    aquatic_background = [rectangle("deepskyblue", get_width(), get_height()),
                          image("https://clipart-library.com/images_k/seaweed-transparent-background/seaweed-transparent-background-2.png",
                              get_width() * 0.8, get_height() + 20),
                          image("https://clipart-library.com/images_k/seaweed-transparent-background/seaweed-transparent-background-2.png",
                              get_width() - get_width() * 0.82, get_height() + 20)]
    return GameScreen(hook_catch_zone, aquatic_background, True, create_hook(), [], [], False, False, HOOK_SPEED,
                      high_score, 0, TIMER, create_sky(), SCENE_DELAY)


def create_score_screen(caught_fish_num: int, high_score: int) -> ScoreScreen:
    """
        Creates the score screen displaying the number of fish the player caught as well as their high score
        :return DesignerObject: the score page
        """
    return ScoreScreen([rectangle("deepskyblue", get_width(), get_height()),
                        rectangle("yellow", get_width() * 0.8, get_height() * 0.8)],
                       text("black", "You caught " + str(caught_fish_num) + " fish!", 45, None,
                            get_height() * (1 / 3),"midbottom", "ComicSans"),
                       emoji("fish"),
                       text("black", "High Score: " + str(high_score) + " fish", 30, None,
                            get_height() * (2 / 3),"midbottom", "ComicSans"),
                       make_button('Start', int(get_width() * 1 / 3), int(get_height() * 3 / 4)),
                       make_button('Quit', int(get_width() * 2 / 3), int(get_height() * 3 / 4)),
                       high_score)


def check_high_score(current_score: int, high_score: int) -> int:
    """
    Updates the highest score if the current score is higher
    :param current_score: the number of fish caught that round
    :param high_score: highest score (highest num of fish caught) on record from previous rounds
    :return: the higher score between the current_score and high_score
    """
    if current_score > high_score:
        return current_score
    else:
        return high_score


def title_screen_to_game(title_world: TitleScreen):
    """
    Switches from the title scene to the game scene when the start button is pressed, and ends the game if the quit
    button is pressed.
    """
    if colliding_with_mouse(title_world.start_button.background):
        change_scene('game', high_score=0)
    if colliding_with_mouse(title_world.quit_button.background):
        quit()
    return


def game_to_score_screen(game_world: GameScreen):
    """
    Switches from the game scene to the score scene when called.
    """
    higher_score = check_high_score(game_world.caught_fish_num, game_world.high_score)
    change_scene('score', caught_fish_num=game_world.caught_fish_num, high_score=higher_score)
    return


def score_screen_to_game(score_screen: ScoreScreen):
    """
    Switches from the score scene to the game scene when the start button is pressed, and ends the game if the quit
    button is pressed.
    """
    if colliding_with_mouse(score_screen.start_button.background):
        change_scene('game', high_score=score_screen.high_score)
    if colliding_with_mouse(score_screen.quit_button.background):
        quit()
    return


def create_hook() -> DesignerObject:
    """Creates and returns the hook"""
    hook = image("https://images.emojiterra.com/openmoji/v13.1/512px/1fa9d.png")
    shrink(hook, 3)
    hook.anchor = "midtop"
    return hook


def create_catch_zone() -> DesignerObject:
    """Creates the zone on the hook where fish collide and are caught (width and height are arbitrary)"""
    return rectangle("deepskyblue", 10, 10)


def adjust_catch_zone(game_world: GameScreen):
    """
    Sets the width and height of the catch zone and moves the catch zone in relation to the hook as the game updates
    :param game_world: the GameScreen instance
    """
    game_world.catch_zone.x = game_world.hook.x - 20
    game_world.catch_zone.y = game_world.hook.y + game_world.hook.height * (3 / 4)
    game_world.catch_zone.width = game_world.hook.width // 3
    game_world.catch_zone.height = game_world.hook.height // 4
    return


def create_sky():
    """Creates and returns the sky and boat image"""
    sky = image("https://www.shutterstock.com/image-vector/seamless-sky-daytime-illustration-600nw-359055326.jpg",
                  None, -get_height(), anchor="center")
    sky.scale = 1.4
    boat = image("https://www.seekpng.com/png/full/832-8329486_fishing-boat-clipart-father-and-son-fishing-boat.png",
                  None,-get_height(), anchor= "center")
    boat.scale = .15
    boat.y = sky.y + 180
    return [sky, boat]


def move_hook(game_world: GameScreen, direction: int):
    """
    Moves the hook horizontally
    :param game_world: the GameScreen instance
    :param direction: either -1, 0, or 1 indicating left-, no movement, or right-facing movement
    """
    game_world.hook.x += game_world.hook_speed * direction
    return


def hook_at_left_edge(game_world: GameScreen):
    """
    Prevents the hook from moving beyond the left wall of the window
    :param game_world: the GameScreen instance
    :return bool: returns true if the hook is nearly touching the left wall of the window; returns false otherwise.
    """
    if game_world.hook.x < game_world.hook.width / 2.9:
        game_world.hook_move_left = False
        return True
    else:
        return False


def hook_at_right_edge(game_world: GameScreen):
    """
    Prevents the hook from moving beyond the right wall of the window
    Returns: returns true if the hook is nearly touching the right wall of the window; returns false otherwise.
    :param game_world: the GameScreen instance
    """
    if game_world.hook.x > get_width() - game_world.hook.width / 4.5:
        game_world.hook_move_right = False
        return True
    else:
        return False


def set_hook_direction(game_world: GameScreen):
    """
    Determines the direction of hook path according to arrow key input and whether the function is at a window boundary,
    then it moves the hook accordingly by calling the move_hook function.
    :param game_world: the GameScreen instance
    """
    if game_world.hook_move_left and (not hook_at_left_edge(game_world)):
        move_hook(game_world, -1)
    elif game_world.hook_move_right and (not hook_at_right_edge(game_world)):
        move_hook(game_world, 1)
    else:
        move_hook(game_world, 0)
    return


def keys_down(game_world: GameScreen, key: str):
    """
    When a right or left arrow key is pressed, the respective boolean variable that determines if the hook should move
    right or left is set to true
    :param game_world: the GameScreen instance
    :param key: the key that was pressed
    """
    if key == "left":
        game_world.hook_move_left = True
    elif key == 'right':
        game_world.hook_move_right = True
    return


def keys_released(game_world: GameScreen, key: str):
    """
        When a right or left arrow key is released, the respective boolean variable that determines if the hook should
        move right or left is set to false
        :param game_world: the GameScreen instance
        :param key: the key that was pressed
        """
    if key == "left":
        game_world.hook_move_left = False
    elif key == 'right':
        game_world.hook_move_right = False
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


def spawn_fish(game_world: GameScreen):
    """
    Spawn a new fish at a random time if there aren't enough fish on the screen
    :param game_world: the GameScreen instance
    """
    not_too_many_fish = len(game_world.fish) < FISH_SPAWN_CAP
    random_chance = randint(1, 15) == 1
    if not_too_many_fish and random_chance:
        game_world.fish.append(create_fish())
    return


def move_fish_horizontally(game_world: GameScreen):
    """
    Moves the fish either right or left depending on which way they're facing
    :param game_world: the GameScreen instance
    """
    for fish in game_world.fish:
        if fish.flip_x:
            fish.x += FISH_SPEED
        else:
            fish.x -= FISH_SPEED
    return


def bounce_fish(game_world: GameScreen):
    """
    Prevents the fish from moving beyond the left or right wall of the window by flipping them around
    :param game_world: the GameScreen instance
    """
    for fish in game_world.fish:
        if fish.x > get_width():
            fish.flip_x = False
        elif fish.x < 0:
            fish.flip_x = True
    return


def make_fish_fall(game_world: GameScreen):
    """
    Moves the fish and seaweed downward across the screen
    :param game_world: the GameScreen instance
    """
    for fish in game_world.fish:
        fish.y += DOWN_SPEED
    for element in game_world.aquatic_background[1:]:
        element.y += DOWN_SPEED
    return


def wrap_fish(game_world: GameScreen):
    """
    Fish wrap around to the top of the screen when they've passed the bottom edge of the window
    :param game_world: the GameScreen instance
    """
    for fish in game_world.fish:
        if fish.y > get_height() + 10:
            fish.y = 0
    return


def track_time(game_world: GameScreen):
    """
    Stops gameplay when the timer has counted down to 0
    :param game_world: the GameScreen instance
    """
    game_world.time -= 1
    if game_world.time <= 0:
        game_world.play = False
    return


def start_animation(game_world: GameScreen):
    """
    When the gameplay condition is true, start_animation calls functions related to fish creation & movement,
    hook & catch zone movement, and the timer countdown.
    :param game_world: the GameScreen instance
    """
    if game_world.play:
        set_hook_direction(game_world)
        spawn_fish(game_world)
        wrap_fish(game_world)
        adjust_catch_zone(game_world)
        track_time(game_world)
    return


def fish_caught_by_hook(game_world: GameScreen):
    """
    Increases score when a fish collides with the hook's catch zone and calls a function to destroy caught fish by
    adding them to the caught_fish list
    :param game_world: the GameScreen instance
    """
    caught_fish = []
    for fish in game_world.fish:
        if colliding(fish, game_world.catch_zone):
            caught_fish.append(fish)
            game_world.caught_fish_num += 1
    game_world.fish = destroy_caught_fish(game_world, game_world.fish, caught_fish)
    return

def destroy_caught_fish(game_world: GameScreen, all_fish: list[DesignerObject], caught_fish: list[DesignerObject]) -> list[DesignerObject]:
    """
    Helper function that adds all fish that have been caught by the hook to the game_world caught_fish list
    :param game_world: the GameScreen instance
    :param all_fish: the original list of fish (both caught fish and free fish)
    :param caught_fish: a list of fish that have been caught by the hook
    :return remaining fish: returns only the fish that haven't been caught
    """
    remaining_fish = []
    for item in all_fish:
        if item in caught_fish:
            game_world.caught_fish.append(item)
        else:
            remaining_fish.append(item)
    return remaining_fish


def position_caught_fish_on_hook(game_world: GameScreen):
    """
    Positions the caught fish on the hook and animates them to look like they're flopping
    :param game_world: the GameScreen instance
    """
    if game_world.caught_fish:
        for fish in game_world.caught_fish:
            fish.angle = -90
            fish.x = randint(game_world.catch_zone.x - 1, game_world.catch_zone.x + 16)
            fish.y = game_world.catch_zone.y + game_world.catch_zone.height
    return


def move_sky_at_end(game_world: GameScreen):
    """
    Manages the end game animation in which the sky and boat come down from top screen, stopping when they collide
    with the hook
    :param game_world: the GameScreen instance
    """
    sky = game_world.sky_elements[0]
    boat = game_world.sky_elements[1]
    if game_world.time <= 25:
        if not colliding(game_world.catch_zone, boat) and not colliding(game_world.hook, sky):
            for element in game_world.sky_elements:
                element.y += 5
        else:
            delay_screen_switch(game_world)
    return


def delay_screen_switch(game_world: GameScreen):
    """
    Delays the appearance of the score screen until the scene_delay reaches 0
    :param game_world: the GameScreen instance
    """
    if game_world.scene_delay <= 0:
        game_to_score_screen(game_world)
    else:
        game_world.scene_delay -= 1
    return


when('starting: title', create_title_screen)
when('clicking: title', title_screen_to_game)
when('starting: game', create_game_screen)
when('starting: score', create_score_screen)
when('clicking: score', score_screen_to_game)
when('typing', keys_down)
when('done typing', keys_released)
when("updating: game", start_animation)
when('updating: game', move_fish_horizontally)
when("updating: game", bounce_fish)
when("updating: game", make_fish_fall)
when("updating: game", fish_caught_by_hook)
when("updating: game", position_caught_fish_on_hook)
when("updating: game", move_sky_at_end)
start()
