""" This program uses randomly generated functions to create colorful artwork. The functions are
    recursive combinations of multiplication, averaging, sin(pi*x), and cos(pi*x)"""

import random
import math
from PIL import Image


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    # I really have no idea how to test this one, other than running it to check that it has
    # the correct recursive depth
    function_elements = ["prod", "avg", "cos_pi", "sin_pi", "cube", "stand"]
    basic_elements = ["x", "y"]
    all_elements = function_elements + basic_elements

    if max_depth == 1:
        return random.choice(basic_elements)
        #Base case: everything needs an 'x' or 'y'
    elif min_depth > 1:
        function = [random.choice(function_elements)]
        #Top level function for this level of recursion
        function = continue_random_function(function, min_depth, max_depth)
    else:
        function = [random.choice(all_elements)]
        function = continue_random_function(function, min_depth, max_depth)

    return function


def continue_random_function(function, min_depth, max_depth):
    """ Takes a function that has been chosen randomly, determines
        how many arguments it needs, and continues to build the
        function with the appropriate level of recursion.
    """
    if function == ["prod"] or ["avg"]:
        function.append(build_random_function(min_depth-1, max_depth-1))
        function.append(build_random_function(min_depth-1, max_depth-1))
        #selects two functions to use
    else:
        function.append(build_random_function(min_depth-1, max_depth-1))
    return function


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
        >>> evaluate_random_function(["prod",["x"],["y"]],1,2)
        2
        >>> evaluate_random_function(["avg",["x"],["y"]],1,2)
        1.5
        >>> evaluate_random_function(["sin_pi",["x"]],1,1)
        0
        >>> evaluate_random_function(["cos_pi",["x"]],1,1)
        -1.0
        >>> evaluate_random_function(["prod",["sin_pi",["x"]],["cos_pi",["x"]]],1,1)
        0
    """
    #Added tests for all the functions, as well as recursion. Sin_pi seems to constantly fail
    #because of a rounding error, but it's obvious that that is what happened.
    if f[0] == "x":
        return x
    elif f[0] == "y":
        return y
    #These are the two basic functions, that will always be used eventually

    elif f[0] == "prod":
        return evaluate_random_function(f[1], x, y)*evaluate_random_function(f[2], x, y)
    elif f[0] == "avg":
        return .5*(evaluate_random_function(f[1], x, y) + evaluate_random_function(f[2], x, y))
    elif f[0] == "cos_pi":
        return math.cos(math.pi*evaluate_random_function(f[1], x, y))
    elif f[0] == "sin_pi":
        return math.sin(math.pi*evaluate_random_function(f[1], x, y))
    elif f[0] == "cube":
        return evaluate_random_function(f[1], x, y)**3
    elif f[0] == "stand":
        return math.sin((3.0/2)*math.asin(evaluate_random_function(f[1], x, y)))
    else:
        print 'f[0] is:\n', f[0]
        return None
        #This will break everything, but it'll do in in a distinctive way, so
        #it'll be easy to track down the bug if it occurs here


def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
        >>> remap_interval(-1, -5, 5, 0, 10)
        4.0
    """
    #Added a doctest to examine negative intervals.
    scale_initial = input_interval_end-input_interval_start
    scale_final = output_interval_end - output_interval_start
    value_initial = val - input_interval_start
    value = value_initial*scale_final/float(scale_initial) + output_interval_start
    return value


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    #import doctest
    #doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    for i in range(15):
        generate_art("New_Art_%d.png" % i)

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
