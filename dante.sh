#!/usr/bin/bash
if command -v pypy &> /dev/null
then
    PYTHON=pypy
else
    PYTHON=python
fi

$PYTHON $PWD/main.py $@