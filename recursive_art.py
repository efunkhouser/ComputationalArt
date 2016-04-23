""" TODO: Put your header comment here """

import random
from math import *
from PIL import Image

class Func(object):
	''' This is a function with a name that tells you how to eval its arguments in the method evaluate_me
		min_depth and max_depth tell you how many functions deep the objects should nest
		Once max_depth is reached, the Func evaluates to arg x or y '''
	
	def __init__(self, func_name, min_depth, max_depth, arg1=None, arg2=None):
		self.func_name = func_name
		self.min_depth = min_depth
		self.max_depth = max_depth
		self.arg1 = arg1 #This will refer to a Func object unless func_name is x or y
		self.arg2 = arg2 #Same here, but only if func_name dictates 2 args

	def __str__(self):
		return self.func_name

	def build_argument_Func(self):
	    """ Builds an association to argument function(s) by creating them as Func object(s)
	    	Returns nothing, just creates those attributes """

	    if self.max_depth==1:
	        funcList = ["x","y"]	    
	    elif self.min_depth <= 1:
	    	funcList = ["x", "y", "prod", "avg", "cos_pi", "sin_pi", "e_expon", "combo"]
	    else:
	    	funcList = ["prod", "avg", "cos_pi", "sin_pi", "e_expon", "combo"]
	    
	    if self.func_name in ["prod", "avg", "combo"]:
	    	self.arg1 = Func(random.choice(funcList), self.min_depth-1, self.max_depth-1)
	    	self.arg2 = Func(random.choice(funcList), self.min_depth-1, self.max_depth-1)
	    else:
	    	self.arg1 = Func(random.choice(funcList), self.min_depth-1, self.max_depth-1)

	def evaluate_me(self,x,y):
	    """ If it's an edge case (x or y), return that
	    	Otherwise:
	    	First generate arguments to evaluate, then
	    	Evaluate this function with inputs x,y
	        Returns: the function value """


		##EDGE CASES
	    if self.func_name == "x":
	    	return x
	    elif self.func_name == "y":
	    	return y


	    if self.arg1 == None:
	    	self.build_argument_Func()
	    	
	    ##RECURSIVE CASES
	    if self.func_name == "cos_pi":
	    	return cos(pi * self.arg1.evaluate_me(x,y))
	    if self.func_name == "sin_pi":
	    	return sin(pi * self.arg1.evaluate_me(x,y))
	    if self.func_name == "e_expon":
	    	return 2.3*(exp(self.arg1.evaluate_me(x,y)-1.0) - 0.567)
		if self.func_name == "prod":
			return self.arg1.evaluate_me(x,y) * self.arg2.evaluate_me(x,y)
	    if self.func_name == "avg":
	    	return 0.5 * (self.arg1.evaluate_me(x,y) + self.arg2.evaluate_me(x,y))
	    if self.func_name == "combo":
			return 0.5 * self.arg1.evaluate_me(x,y)**2 + 0.5 * cos(self.arg2.evaluate_me(x,y))

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
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
    """
    val = float(val)
    input_interval_start = float(input_interval_start)
    input_interval_end = float(input_interval_end)
    output_interval_start = float(output_interval_start)
    output_interval_end = float(output_interval_end)

    slope = (output_interval_end - output_interval_start)/(input_interval_end - input_interval_start)
    f = slope*(val - input_interval_end) + output_interval_end
    return f


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
    # NOTE: This relies on remap_interval, which you must provide
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
    funcList = ["prod", "avg", "cos_pi", "sin_pi", "e_expon", "combo"]
    red_function = Func(random.choice(funcList), 7, 9)
    green_function = Func(random.choice(funcList), 7, 9)
    blue_function = Func(random.choice(funcList), 7, 9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(red_function.evaluate_me(x, y)),
                    color_map(green_function.evaluate_me(x, y)),
                    color_map(blue_function.evaluate_me(x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("please.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
