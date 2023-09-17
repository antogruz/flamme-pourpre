# flamme-pourpre
Play the game Flamme Rouge

## User
Run ./play.sh to start a game. You have Green Riders.

## Developer
There are 4 entry points
 - **check.sh** runs all unit tests
 - **visualcheck.sh** shows some displays features, to control that UI is still nice
 - **play.sh** lets you play a game
 - **integrationTests.sh** to check that the game works with everything well integrated
 
The engine of the game is in **jeu/**. This directory has no dependency.
The display of the game is in **beau/**. It depends on **jeu/** and on tkinter.
The animations are in **animate/**. It depends on **beau/**.
The final assembly of all the components that let you play is in **main/**. It depends on everything.
In **tk/**, there are some examples of tkinter usages, but not related to Flamme Rouge.
