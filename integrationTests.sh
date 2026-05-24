#!/bin/bash

cd "$(dirname "$0")"
PYTHONPATH=$PYTHONPATH:.:engine/:jeu/:beau/:creation/:animate/:homeMadeUI/:main/ python3 main/integrationTests.py $@
