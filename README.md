# Atomic Chess

A two-player desktop game of atomic chess, built with Python and Pygame. Atomic chess is a chess variant where every capture triggers an explosion.

## Features
- Drag-and-drop piece movement with highlighted legal moves and last move
- Atomic explosions: a capture removes the capturing piece, the captured piece, and every adjacent non-pawn enemy piece
- King safety: each candidate move is simulated on a copy of the board, and moves that leave your king attacked are rejected
- The game ends on checkmate, stalemate, or an exploded king, with a winner banner
- Move and capture sound effects

## Run it
You need Python 3. From the project's root folder:

```bash
pip install pygame
python src/main.py
```

Run it from the root folder, because the game loads its images and sounds with relative paths.

## How it's organized
| File | Role |
| --- | --- |
| `src/main.py` | Game loop and mouse events |
| `src/game.py` | Drawing, turns, and game-over detection |
| `src/board.py` | Move generation, explosions, and check detection |
| `src/piece.py` | Piece classes and values |
| `src/square.py`, `src/move.py` | Board squares and moves |
| `src/dragger.py` | Drag-and-drop state |
| `src/config.py`, `src/sound.py` | Audio |
| `src/const.py` | Window and board dimensions |

## Rules notes
- In this version an explosion removes only the opponent's adjacent pieces. Standard atomic chess also removes your own.
- Kings cannot capture, since the capturing piece explodes too.
- Not yet implemented: castling, en passant, pawn promotion, and an AI opponent.

## Credits
Built on the structure of a Pygame chess tutorial: https://youtu.be/OpL0Gcfn4B4?t=11970. The atomic rules, check detection, and win conditions were added on top.
