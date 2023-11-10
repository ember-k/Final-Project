# Ember Kerstetter's Final-Project
This repository will be used to store all of the code for the features and functons of the game I will design for my final project.
# emberk@udel.edu

# Fishing Game
This game is inspired by online fishing games where the player controls a hook that is cast into a body of water. The screen starts
with the hook at a deep depth in the water, so much so that the fisherman and boat can't be seen in the window. As the time passes, 
the background/fish frame moves down giving the hook the appearance that it is being reeled upwards. the player must use their mouse
to drag the hook left and right to catch fish as the hook makes its way up to the surface. The goal of this game is to use the hook to
catch as many fish as possible before the hook is reeled back to the surface (progressively faster and faster). Points depend on the 
type of fish in addition to the number of fish caught.

# Phase 1
- [x] Play screen: the opening window with a high score counter and a play button (player presses the space bar)
- [x] Setting: Program the aquatic background
- [ ] Hook exists: at the start of the round and can't be moved vertically from its position (only right or left) 
(My TA suggested that I don't do the animation of the hook descending)
- [x] Hook movement: The player can use the arrow keys to move the hook left and right (I might try to get dragging to work as a bonus in phase 3)
- [x] Screen limits: the hook can't be moved off-screen (the hook can't move further once it hits the side)
- [x] Fish exist: Fish appear from either side of the screen

# Phase 2
- [ ] Fish move: fish move left and right across the screen while moving generally downwards
- [ ] fish wrap: if fish move down to the bottom of the screen, they wrap back to the top
- [ ] Screen limits: fish can't move off screen
- [ ] fish collision: When the hook touches a fish, points are gained and the type & number of fish collisions are recorded.
- [ ] Max collisions: Only a certain number of fish can be caught before the hook is full


# Phase 3
- [ ] Hooked Fish movement: When fish collide with the hook, they are relocated to align their movements with the hook.
  (They appear to be hanging on the hook and get dragged with the hook like in real fishing)
- [ ] Water's Surace: After a certain amount of time, the surface of the water should descend from the top of the screen until it
  collides with the hook, then the game pauses
- [ ] End of Round: A message displays when the hook collides with the water's surface. The number and type of fish that were caught are
  displayed along with the total points that were earned
- [ ] Update Play screen: Play screen is updated with cumulative points and the player is given the option to play another round.
- [ ] (Nice to have) Rare fish: rare fish are added that are smaller and/or move across the screen faster which are worth extra points
