#!/usr/bin/env bash

CASE=$1
PARAMETERS=$2
STUDY_NAME=$3


for i in 2 4 6 8 10;
do
    pyFoamRunParameterVariation.py --every-variant-one-case-execution \
        --create-database \
        --no-execute-solver \
        --no-server-process \
        --cloned-case-prefix=$STUDY_NAME \
        --single-variation=$i \
        $CASE \
        $PARAMETERS
done 
