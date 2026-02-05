# Python-Linguistic-Vocabulary-Game
A python game for learning vocabularies for a linguistic course

## Used Libraries:
- Pygame
- Pygame_menu

## Structure of our Game
Menu: The main menu of our game is a slightly edited version of the default pygame_menu menu.
Game: This class keeps track of the score and starts each game.
- HogansAlley
- QuickieQuiz
- PraiseOrHaze

## Inspiration and Concept
The inspiration to our game comes mostly from a Microgame collection from the game "Wario Ware", where players must react quickly to very short and simple tasks ranging from 2 to 5 seconds. We choose this idea because short games it makes it easy to replay the tasks for memorizing vocabulary and small scope grammar. This keeps users motivated to keep on learning by playing the games.

## What did each of us do?

### David
- PraiseOrHaze
- Boss
- Fonts
- Transitions
In the beginning i had mny problems with the right scaling of the sprites and getting the, which got much more easily with time and a sort of feeling for the number to use to move sprites around. The main issues was the Main Game logic, escpecially what party of the minigames we could put in the Game class to reuse in the otehr minigames. My biggest encounter was the creating of the Font. I researched and tried quite a while until i got it to work. It scann though the font sprite line for line with the first pixel in the left upper corner as "Background" and ends a symbol once it detect a Background pixel after detecting a not Background pixel. I alligned all symbols to the bottom line, why letters like "g" and "y", which should be below the bottom textline are kind of "levitating" and look a bit weird. Unfortuantly the Font couldn't be used in the menu, because the pygame menu only allows its own and system font, why we used teh 8-Bit Font which suited the best, we thought. Another big problem I run into was crashing during animation, if clicked anything. Escpecially in the Boss game i had many issues with animation crashes or overlaping. But most of these Problems were later solved by putting boolean states during animation, during which the player input was completly blocked. But some errors remained if the PLayer clicks something during a specific moment like in the Boss game during The Boss spwn it resets the game.

### Pascal
- This
- Thas

## Interesting Codesnippets
### Combining dicts

    if len(options_list) == 2:
        positions = ["left", "right"]
    else:
        positions = ["top", "bottom", "left", "right"]

    random.shuffle(positions)

    options = dict(zip(positions, options_list))


### Together
- The Main logic in Game
- The Menu
- very much troubleshooting

## Documentation




Refactored code: abstract classes: CheckAnswer