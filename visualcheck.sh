#!/bin/bash

for f in beau/*.py ; do
    PYTHONPATH=$PYTHONPATH:jeu/ python3 $f
done

for f in animate/*.py ; do
    PYTHONPATH=$PYTHONPATH:jeu/:beau/ python3 $f
done

