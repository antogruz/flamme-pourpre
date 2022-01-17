# flamme-pourpre
Play the game Flamme Rouge

## User
Run ./play.sh to start a game. You have Green Riders.

## Developer
There are 3 entry points
 - **check.sh** runs all unit tests
 - **visualcheck.sh** shows some displays features, to control that UI is still nice
 - **play.sh** lets you play a game. You can specify **--faster N** to run it automatically, and **N** times faster
 
The engine of the game is in **jeu/**. This directory has no dependency.
The display of the game is in **beau/**. It depends on **jeu/** and on tkinter
In **tk/**, there are some examples of tkinter usages, but not related to Flamme Rouge.
