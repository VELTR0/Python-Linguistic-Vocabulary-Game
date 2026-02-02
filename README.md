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
- Praise Or Haze

### Pascal
- Quickie Quiz
- Hogans' Alley

## Interesting Codesnippets
### Combining dicts

    if len(options_list) == 2:
        positions = ["left", "right"]
    else:
        positions = ["top", "bottom", "left", "right"]

    random.shuffle(positions)

    options = dict(zip(positions, options_list))





Refactored code: abstract classes: CheckAnswer