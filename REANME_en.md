HunterChess
===========

A tiny chess game based on python,wxpython


How to play:
===========
Player black goes first.Click to select, move.Doubleclick to undo.


Rules:
===========
1,Player moves take turns
2,When player1 moved,take a look at the last move.
  If two pieces(must include the last move) of player1 are against only one piece of player2 in a row (or in a line),
  then the one piece of player2 will be eaten.
  It's same when player2 moves. 
3,When one player's pieces were all eaten, another player wins.

Examples:
============

case1：

Player1 move to (0,3), player2 at (2,3) will be eaten.

[1, 1, 0, 1]

[0, 0, 0, 1]

[0, 0, 0, 2]

[2, 2, 0, 0]

case2：

Player1 move to (0,0), player2 at (2,3) will NOT be eaten.

[1, 1, 0, 1]

[0, 0, 0, 1]

[0, 0, 0, 2]

[2, 2, 0, 0]

case3：

Player1 move to (0,3), player2 at (2,3) will  NOT be eaten.
[1, 1, 0, 1]

[0, 0, 0, 1]

[0, 0, 0, 2]

[2, 2, 0, 2]


case4：

Player1 move to (2,3), player2 at (3,3) will NOT be eaten.
[1, 1, 0, 2]

[0, 0, 0, 1]

[0, 0, 0, 1]

[2, 2, 0, 2]

case5：

Player2 move to (0,3), player2 at (2,3) will NOT be eaten.

[1, 1, 0, 0]

[0, 0, 0, 1]

[0, 0, 0, 1]

[2, 2, 0, 2]

It's the same on columns.

Python   ：2.7.2
Depends  ：wxpython
exe file : pyinstaller