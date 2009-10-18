#!/usr/bin/bash
# This is an example of a test script
lamboot $PBS_NODEFILE

mpirun C myprog

lamhalt
