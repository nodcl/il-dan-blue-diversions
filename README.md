# il-dan-blue-diversions

This repo contains two command line utilities: `blue_feet_numeric.py` and `blue_feet_symbolic.py`.  The former is by far the more polished and developed utility. Both model the progression of foot positions for the Choi Kwang-Do Il Dan Blue pattern. It created these both to help me understand the pattern better, and as a fun math and programming exercise.


# blue_feet_numeric.py
This utility requires one to specify the left-right and front-back distance between your feet, as well as whether to the right or left side of the pattern is to be computed. It then prints the left and right foot positions after each kick. This utility requires the Python `numpy` package. For a description of the command line options do `blue_feet_numeric.py --help`.


# blue_feet_symbolic.py
This utility was my first attempt to use CAS to determine the movement matrices for each of the kicks in the pattern. While the matrices are computed quickly, the expressions end up being so complicated that my poor little laptop cannot print them. Or at least, I'm not willing to wait the time it would take to print them. This utility requires the Python `sympy` package. I include it in this repo mostly for posterity, should I ever want to come back to refresh what I learned about using `sympy`.
