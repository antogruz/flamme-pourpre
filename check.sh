#!/bin/bash

set -e

for f in jeu/*.py specialTour/*.py specialTour/**/*.py; do
    PYTHONPATH=$PYTHONPATH:jeu/ python3 $f
done
