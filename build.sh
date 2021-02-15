#!/bin/bash

ARGS="$@"
PATH_VENV_DIR=`make venv-path`

source $PATH_VENV_DIR/bin/activate && make $ARGS
