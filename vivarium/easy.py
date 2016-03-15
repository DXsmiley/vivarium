"""The simplest way to use vivarium.

`easy` contains a few functions that make vivarium easier to use.
By using these functions, power and control is sacrificed.

"""


import vivarium.transform
import vivarium.core
import vivarium.scope
import vivarium.pipes

def run(code, input_data = None, do_print = True):
	"""Execute code and return the result.

	By default, the program will be able to read from standard input, through `input` and write to standard output, via `print`.
	The function will return a list of strings produced by calles to the `print` function.

	Arguments:
	code -- Python code to run (as a string)

	Keyword arguments:
	input_data -- A list of strings that will be given to the program as it call the `input` function.
		If it attempts to read more input than is given, an exception will be thrown and the program will terminate.
	do_print -- A boolean specifying whether calls to `print` should actually print to standard output. True by default. 
	"""
	# Set up the scope
	globs = vivarium.scope.global_scope()
	output = vivarium.pipes.Output(scope = globs)
	if input_data is not None:
		vivarium.pipes.Input(input_data, globs)
	program_scpe = vivarium.scope.Scope(globs)
	globs.lockdown()
	# Compile and run
	bytecode = vivarium.transform.transform(code)
	bytecode.evaluate(program_scpe)
	# Return output
	return output.get_data()

def run_from_file(filename, input_data = None, do_print = True):
	"""Execute code from a file and return the result.

	`filename` should be the path to the file which contains the code.

	Functionality and keyword arguments are the same as `run`.
	"""
	with open(filename) as f:
		code = f.read()
	return run(code, input_data = input_data, do_print = do_print)