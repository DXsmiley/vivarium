# These can be used to either send data into the program as input,
# or to capture the output of the program.

import vivarium.data.function

class Output:

	def __init__(self, display = True, scope = None):
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
		return self.output

class Input:

	def __init__(self, lines, scope = None):
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