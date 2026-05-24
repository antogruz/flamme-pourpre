#!/bin/bash

cd "$(dirname "$0")"
PYTHONPATH=$PYTHONPATH:.:engine/:jeu/:beau/:animate/:beau/decorators/:homeMadeUI/:main/ python3 main/launcher.py $@
