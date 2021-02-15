#!/usr/bin/env python3
from sympy import *
import pdb

init_printing(use_unicode=True)

m, n = symbols('m n')

#theta1 = (pi/2) - atan(m/n)
#theta2 = ((3 * pi) / 2) - theta1

theta1, theta2 = symbols('theta1 theta2')

swingkick = Matrix([[cos(theta1), -sin(theta1), 0],
                    [sin(theta1), cos(theta1), 0],
                    [0, 0, 1]])

rsidekick = Matrix([[cos(theta2), -sin(theta2), 0],
                    [sin(theta2), cos(theta2), 0],
                    [0, 0, 1]])

def do_swingkick(curpos):

    x1 = curpos[0,1]
    y1 = curpos[1,1]

    T1 = Matrix([[1, 0, x1],
                 [0, 1, y1],
                 [0, 0, 1]])

    T2 = Matrix([[1, 0, -x1],
                 [0, 1, -y1],
                 [0, 0, 1]])

    newpos = T1 * swingkick * T2 * curpos

    return newpos

def do_rsidekick(curpos):

    x1 = curpos[0,0]
    y1 = curpos[1,0]

    T1 = Matrix([[1, 0, x1],
                 [0, 1, y1],
                 [0, 0, 1]])

    T2 = Matrix([[1, 0, -x1],
                 [0, 1, -y1],
                 [0, 0, 1]])

    newpos = T1 * rsidekick * T2 * curpos

    return newpos


x1a, y1a, x1b, y1b = symbols('x1a y1a x1b y1b')

initpos = Matrix([[x1a, x1b], [y1a, y1b], [1, 1]])
print('Computing move 1...')
move1 = do_swingkick(initpos)
print('Computing move 2...')
move2 = do_rsidekick(move1)
print('Computing move 3...')
move3 = do_swingkick(move2)
print('Computing move 4...')
move4 = do_rsidekick(move3)
print('Computing move 5...')
move5 = do_swingkick(move4)
print('Computing move 6...')
move6 = do_rsidekick(move5)
print(move6)
print('Computing move 7...')
move7 = do_swingkick(move6)
print('Computing move 8...')
move8 = do_rsidekick(move7)
#print('Trying to simplify...')
#move8 = simplify(move8)
print('Trying to print result...')
print(move8)
