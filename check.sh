#!/bin/bash

set -e

for f in jeu/*.py ; do
    python3 $f
done
