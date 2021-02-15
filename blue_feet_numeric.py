#!/usr/bin/env python3
import argparse
import pdb
import numpy as np

CHOICE_LEFT = 'left'
CHOICE_RIGHT = 'right'
CHOICES_LR = [CHOICE_LEFT, CHOICE_RIGHT]


class FLSwingKickToSideStance:
    """Models the 2d motion of a front-leg swing kick landing in side-stance

    This class models the two dimensional motion of a front-leg swing kick
    that lands in a side-stance. An instance of this class is initialized
    by indicating which leg is kicking and the distances between the feet.
    """

    LEFT_LEG = 0
    RIGHT_LEG = 1

    legs = {'left': LEFT_LEG,
            'right': RIGHT_LEG}

    def __init__(self, kicking_leg, dist_leftright, dist_frontback):
        """Constructor for FLSwingKickToSideStance

        Instantiates a new FLSwingKickToSideStance object

        Args:
            kicking_leg(str): The kicking leg. One of {'left', 'right'}.
            dist_leftright(float,int): The left-right distance between your
                                       feet in left-front or right-front
                                       stance.
            dist_frontback(float,int): The front-back distance between your
                                       feet in in left-front or right-front
                                       stance.

        Returns:
          An instance of the FLSwingKickToSideStance class
        """

        if not isinstance(kicking_leg, str):
            raise TypeError('kicking leg must be a string equal to one of '
                            '{{{}}}'.format(', '.join(list(self.legs.keys()))))

        if kicking_leg.lower() not in self.legs:
            raise ValueError('kicking leg must be one of '
                             '{{{}}}'.format(', '.join(list(self.legs.keys()))))

        self.kicking_leg = self.legs[kicking_leg.lower()]

        theta = (np.pi/2) - np.arctan(dist_frontback/dist_leftright)

        self.dist_leftright = dist_leftright
        self.dist_frontback = dist_frontback

        if self.kicking_leg == FLSwingKickToSideStance.RIGHT_LEG:
            self.rotation_matrix = np.array(
                    [[np.cos(theta), -np.sin(theta), 0],
                     [np.sin(theta), np.cos(theta),  0],
                     [0,             0,              1]])
        else:
            self.rotation_matrix = np.array(
                    [[np.cos(theta),  np.sin(theta), 0],
                     [-np.sin(theta), np.cos(theta), 0],
                     [0,              0,             1]])

    def __repr__(self):
        if self.kicking_leg == FLSwingKickToSideStance.LEFT_LEG:
            kleg = 'left'
        else:
            kleg = 'right'

        return 'FLSwingKickToSideStance' \
               '({}, {}, {})'.format(kleg, self.dist_leftright,
                                     self.dist_frontback)

    def kick(self, foot_positions):
        """Computes the new positions of foot_positions after the kick

        This method computes the new foot positions after the kick is
        completed, given the current positions encoded in 'foot_positions'.

        The positions of the left and right feet are expected in columns zero
        and one respectively.

        Row 0 of foot_positions is expected to contain the X Cartesian
        coordinate and row 1 is expected to contain the Y Cartesian coordinate.
        As foot_positions is expected to express positions in homogeneous
        coordinates, each element of row 2 is expected to contain 1.

        Args:
            foot_positions(numpy.array): 3 x 2 array describing the positions
                                         of the left and right feet.

        Returns:
            numpy.array encoding the new position of the left and right feet
            in homogeneous coordinates
        """

        if self.kicking_leg == self.LEFT_LEG:
            # Left leg is kicking so we're rotating in the right leg,
            # whose coordinates are in column 1
            x = foot_positions[0, 1]
            y = foot_positions[1, 1]

        else:
            x = foot_positions[0, 0]
            y = foot_positions[1, 0]

        # T1 undoes the actions of T2, moving the point around which we're
        # rotating away from the origin and back to its original position.
        T1 = np.array([[1, 0, x],
                       [0, 1, y],
                       [0, 0, 1]])

        # T2 moves the point about which we're rotating to the origin.
        # Note the negation of x and y below. That's the magic that moves
        # the point to the origin, preparing it for a rotation.
        T2 = np.array([[1, 0, -x],
                       [0, 1, -y],
                       [0, 0, 1]])

        # '@' is shorthand for np.matmul()
        # I find it easier to read right-to-left below. We translate the
        # leg around which we're rotating to the origin by multiplying
        # T2 by foot_positions. Then we rotate. Then we undo the translation.
        newpos = T1 @ self.rotation_matrix @ T2 @ foot_positions

        return newpos


class SpinningSideKick:
    """Models the 2d motion of a spinning side kick

    This class models the two dimensional motion of a spinning side kick.
    An instance of this class is initialized by indicating which leg is kicking
    and the distances between the feet.
    """

    LEFT_LEG = 0
    RIGHT_LEG = 1

    legs = {'left': LEFT_LEG,
            'right': RIGHT_LEG}

    def __init__(self, kicking_leg, dist_leftright, dist_frontback):
        """Constructor for SpinningSideKick

        Instantiates a new SpinningSideKick object

        Args:
            kicking_leg(str): Which leg is kicking. One of {'left', 'right'}
            dist_leftright(float,int): The left-right distance between your
                                       feet in left-front or right-front
                                       stance.
            dist_frontback(float,int): The front-back distance between your
                                       feetin in left-front or right-front
                                       stance.

        Returns:
          an instance of the SpinningSideKick class
        """

        if not isinstance(kicking_leg, str):
            raise TypeError('kicking leg must be a string equal to one of '
                            '{{{}}}'.format(', '.join(list(self.legs.keys()))))

        if kicking_leg.lower() not in self.legs:
            raise ValueError('kicking leg must be one of '
                             '{{{}}}'.format(', '.join(list(self.legs.keys()))))

        self.kicking_leg = self.legs[kicking_leg.lower()]

        theta = np.pi + np.arctan(dist_frontback/dist_leftright)

        self.dist_leftright = dist_leftright
        self.dist_frontback = dist_frontback

        if self.kicking_leg == SpinningSideKick.LEFT_LEG:
            self.rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                                            [np.sin(theta), np.cos(theta), 0],
                                            [0,          0,                1]])
        else:
            self.rotation_matrix = np.array([[np.cos(theta), np.sin(theta), 0],
                                            [-np.sin(theta), np.cos(theta), 0],
                                            [0,          0,                1]])

    def __repr__(self):
        if self.kicking_leg == SpinningSideKick.LEFT_LEG:
            kleg = 'left'
        else:
            kleg = 'right'

        return 'SpinningSideKick({}, {}, {})'.format(kleg,
                                                     self.dist_leftright,
                                                     self.dist_frontback)

    def kick(self, foot_positions):
        """Computes the new positions of foot_positions after the kick

        This method computes the new foot positions after the kick is
        completed, given the current positions encoded in foot_positions.

        The positions of the left and right feet are expected in columns zero
        and one respectively.

        Row 0 of foot_positions is expected to contain the X Cartesian
        coordinate and row 1 is expected to contain the Y Cartesian coordinate.
        As foot_positions is expected to express positions in homogeneous
        coordinates, each element of row 2 is expected to contain 1.

        Args:
            foot_positions(numpy.array): 3 x 2 array describing the positions
                                         of the left and right feet.

        Returns:
            numpy.array encoding the new position of the left and right feet
            in homogeneous coordinates
        """

        if self.kicking_leg == self.LEFT_LEG:
            # Left leg is kicking so we're rotating in the right leg,
            # whose coordinates are in column 1
            x = foot_positions[0, 1]
            y = foot_positions[1, 1]

        else:
            x = foot_positions[0, 0]
            y = foot_positions[1, 0]

        # T1 undoes the actions of T2, moving the point around which we're
        # rotating away from the origin and back to its original position.
        T1 = np.array([[1, 0, x],
                       [0, 1, y],
                       [0, 0, 1]])

        # T2 moves the point about which we're rotating to the origin.
        # Note the negation of x and y below. That's the magic that moves
        # the point to the origin, preparing it for a rotation.
        T2 = np.array([[1, 0, -x],
                       [0, 1, -y],
                       [0, 0, 1]])

        # '@' is shorthand for np.matmul()
        # I find it easier to read right-to-left below. We translate the
        # leg around which we're rotating to the origin by multiplying
        # T2 by foot_positions. Then we rotate. Then we undo the translation.
        newpos = T1 @ self.rotation_matrix @ T2 @ foot_positions

        return newpos


def pos2str(posarray):
    """Convenience function for printing array values

    Args:
        posarray(np.array): A 2 x 3 array of values to print

    Returns:
        A string encoding the values of posarray
    """

    return 'left ({:.2f}, {:.2f}) ' \
           'right ({:.2f}, {:.2f})'.format(posarray[0, 0], posarray[1, 0],
                                           posarray[0, 1], posarray[1, 1])

def main():

    aparser = argparse.ArgumentParser(description='Computes foot positions '
                                      'for il dan blue pattern')
    aparser.add_argument('-l', '--lrdist', required=True, type=float,
                         help='The left-right distance between your feet in '
                              'left-front or right-front stance')
    aparser.add_argument('-f', '--fbdist', required=True, type=float,
                         help='The front-back distance between your feet in '
                              'left-front or right-front stance')
    aparser.add_argument('-s', '--side', required=True, choices=CHOICES_LR,
                         help='Which side of the pattern to perform')

    args = aparser.parse_args()

    if args.lrdist <= 0.0:
        print('The value of the lrdist(-l) argument must be greater than or '
              'equal to 0.')
        raise SystemExit(1)

    if args.fbdist <= 0.0:
        print('The value of the fbdist(-f) argument must be greater than or '
              'equal to 0.')
        raise SystemExit(1)

    # newpos is initialized to be the Cartesian coordinates of the left and
    # right feet base on the command line arguments provided. In order to
    # perform translations using matrices, we must use 'homogenous
    # coordinates'. Therefore newpos is dimensioned 2 x 3. Column 0 contains
    # the x, y and z coordinates of the left foot whereas column 1 contains the
    # x, y and z coordinates of the right foot.
    #
    # The z coordinate in all cases must be 1 per the rules for using matrices
    # to model translations in the Cartesian plane.

    if args.side == CHOICE_RIGHT:
        flsk = FLSwingKickToSideStance('right', args.lrdist, args.fbdist)
        ssk = SpinningSideKick('left', args.lrdist, args.fbdist)

        # For right side, we'll put the right foot at the origin and the left
        # foot in the third quadrant.
        newpos = np.array([[-args.lrdist, 0],
                           [-args.fbdist, 0],
                           [1, 1]])
    else:
        flsk = FLSwingKickToSideStance('left', args.lrdist, args.fbdist)
        ssk = SpinningSideKick('right', args.lrdist, args.fbdist)

        # For right side, we'll put the left foot at the origin and the right
        # foot in the fourth quadrant
        newpos = np.array([[0, args.lrdist],
                           [0, -args.fbdist],
                           [1, 1]])

    print('Initial position: left {}\n'.format(pos2str(newpos)))

    for direction in ['north', 'east', 'south', 'west']:

        print('Kicking {}'.format(direction))

        newpos = flsk.kick(newpos)
        print('After front-leg swing kick. {}'.format(pos2str(newpos)))

        newpos = ssk.kick(newpos)
        print('After spinning side kick. {}\n'.format(pos2str(newpos)))


if __name__ == '__main__':
    main()
