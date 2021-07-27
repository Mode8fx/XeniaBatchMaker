# Xenia Batch Maker
This is a simple Python script that creates batch files that open Xenia games.

Because Xenia games have to be stored and named in a manner that's not easily readable, and Xenia itself doesn't currently have a UI with a games list, this was made to create batch files that are named after each game's internal name so finding a desired game is much easier.

For example, the following game file:
"C:\Content\0000000000000000\58410912\000D0000\813B8117E82BB641BE619486127F36F3B0EF9D8A58"
... will result in a batch file called "Worms 2 - Armageddon.bat". Running this file will open the desired game in a provided copy of Xenia (or Xenia Canary, whatever you choose).

Note that Xenia games do not have to be stored in the same folder as Xenia, but they must be stored in a "Content/0000000000000000" folder as described above.