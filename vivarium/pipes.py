"""Used to either send data into the program as input, or to capture the output of the program."""

import vivarium.data.function

class Output:
	"""Captures and redirects a program's calls to `print`."""

	def __init__(self, display = True, scope = None):
		"""Create an output pipe.

		Arguments
		display -- Whether output should br forwarded to stdio via the real print function.
			Defaults to True.
		scope -- The scope in which to use the pipe. Usually the program's global scope.
			Defaults to None, in which case the pipe will not assign itself."""
		self.output = []
		self.display = display
		if scope:
			scope.set('print').set(vivarium.data.function.FunctionBuiltin(self))

	def __call__(self, *args):
		s = ' '.join(str(i) for i in args)
		self.output.append(s)
		if self.display:
			print(*args)

	def get_data(self):
		"""Return the output of the program as a list of strings."""
		return self.output

class Input:
	"""Used to send input to a program. Overrides the `input` function."""

	def __init__(self, lines, scope = None):
		"""Create an input pipe.

		Arguments
		lines -- A list of strings. Strings will be passed one at a time, whenever `input` is called.
		scope -- The scope in which to use the pipe. Usually the program's global scope.
			Defaults to None, in which case the pipe will not assign itself.
		"""
		self.lines = lines
		self.current = 0
		if scope:
			scope.set('input').set(vivarium.data.function.FunctionBuiltin(self))

	def __call__(self, *args):
		if self.current == len(self.lines):
			raise Exception('Attempted to read more input than was given.')
		l = self.lines[self.current]
		self.current += 1
		return l