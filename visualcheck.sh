#!/bin/bash

for f in beau/*.py ; do
    PYTHONPATH=$PYTHONPATH:jeu/ python3 $f
done
