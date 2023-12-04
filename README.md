# The Fishing Game
A game in which a player controls a hook to catch as many fish as they can in the given amount of time.
## About
This game is inspired by online fishing games where the player controls a hook that is cast into a body of water. 
The screen starts with the hook at a deep depth in the water, so much so that the fisherman and boat can't be seen in 
the window. As the time passes, the background/fish frame moves down giving the hook the appearance that it is being 
reeled upwards. The player must use move the hook left and right to catch fish as the hook makes its way 
up to the surface. The goal of this game is to catch as many fish as possible before time runs out and the hook is 
reeled back to the surface.


## Preview
Full game preview Youtube link:

## Instructions
1. Once the title screen appears, the player clicks either "quit" to stop or "start" to begin the game
2. Once the game is in progress, the player must use the left and right arrow keys to move the hook in the direction 
they want. (The hook continues moving in the direction of the key pressed until the key is released)
3. Once time runs out, the hook will freeze in place (the player no longer has control of the hook) and the end-scene
animation will play as the hook is reeled to the surface
4. Once the score screen is displayed, the player selects either "quit" if they wish to stop the game, or "start" if
they wish to continue the game.

## Author
Name: Ember Kerstetter

Email: embek@udel.edu

## Acknowledgements
- https://www.coolmathgames.com/0-tiny-fishing#immersiveModal
- https://designer-edu.github.io/designer/contents.html

## Task List

### Phase 1
**Phase 1 YouTube Link: https://youtu.be/y9jnuvG-mws**
- [x] Play screen: the opening window with a high score counter and a play button (player presses the space bar)
- [x] Setting: Program the aquatic background
- [x] Hook exists: at the start of the round and can't be moved vertically from its position (only right or left) 
(My TA suggested that I make the animation of the hook descending a nice-to-get-to bonus step in Phase 3)
- [x] Hook movement: The player can use the arrow keys to move the hook left and right (I might try to get dragging to work as a bonus in phase 3)
- [x] Screen limits: the hook can't be moved off-screen (the hook can't move further once it hits the side)
- [x] Fish exist: Fish appear from either side of the screen



### Phase 2
**Phase 2 YouTube Link: https://youtu.be/sMO5mKqavTs**
- [x] Fish move: fish move left and right across the screen while moving generally downwards
- [x] fish wrap: if fish move down to the bottom of the screen, they wrap back to the top
- [x] Screen limits: fish can't move off screen
- [x] Fish collision: When the hook touches a fish, points are gained and the number of fish collisions are recorded.
- [x] Countdown Timer: Gameplay (fish and hook movement) stops after a certain amount of time has passed 
(I replaced max collisions with countdown timer since it makes more sense for players to try to catch as many fish 
as they can in a given amount of time, rather than have a cap on the number of fish they can catch)


### Phase 3
- [x] Hooked Fish movement: When fish collide with the hook, they are relocated to align their movements with the hook.
  (They appear to be hanging on the hook and get dragged with the hook like in real fishing)
- [x] Water's Surface: After a certain amount of time, the surface of the water should descend from the top of the screen until it
  collides with the hook, then the game pauses
- [x] End of Round: A message displays when the hook collides with the water's surface. The number and type of fish that were caught are
  displayed along with the updated high score.
- [x] Next round option: The high score is kept track of between rounds and the player is given the option to play another round.
- [ ] (Nice to have) Rare fish: rare fish are added that are smaller and/or move across the screen faster which are worth extra points
- [ ] (Nice to have) Hook animation: animation of the hook descending after the start screen disappears
- [ ] (Nice to have) Drag the Hook: Instead of using arrow keys I can have the hook follow where the player drags the mouse
