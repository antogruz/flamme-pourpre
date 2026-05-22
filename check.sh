#!/bin/bash

set -e

for f in jeu/*.py specialTour/*.py specialTour/**/*.py; do
    PYTHONPATH=$PYTHONPATH:jeu/ python3 $f
done

for f in engine/*.py; do
    PYTHONPATH=$PYTHONPATH:jeu/:specialTour/:engine/ python3 $f
done
