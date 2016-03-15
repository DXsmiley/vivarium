import vivarium
import json
import os
import itertools

def open_relative(my_file):
	fn = os.path.join(os.path.dirname(__file__), my_file)
	return open(fn)

class OutputCapture:

	def __init__(self):
		self.output = []

	def __call__(self, *args):
		s = ' '.join(str(i) for i in args)
		self.output.append(s)

class InputPipe:

	def __init__(self, lines, scope = None):
		self.lines = lines
		self.current = 0

	def __call__(self, *args):
		assert self.current < len(self.lines)
		l = self.lines[self.current]
		self.current += 1
		return l

def run_test(name):
	print('Running', n)
	# Load required data
	jdata = json.loads(open_relative(name + '.json').read())
	code = open_relative(name + '.py').read()
	for k, io in enumerate(jdata):
		print('Case', k + 1)
		# print(io)
		globs = vivarium.scope.global_scope()
		bytecode = vivarium.transform.transform(code)
		# Capture the output
		capture = OutputCapture()
		globs.set('print').set(vivarium.data.function.FunctionBuiltin(capture))
		# Pipe the input
		pipe = InputPipe(io['input'])
		globs.set('input').set(vivarium.data.function.FunctionBuiltin(pipe))
		# Run
		globs.lockdown()
		program_scope = vivarium.scope.Scope(globs)
		bytecode.evaluate(program_scope)
		# This should be updated to give more detailed errors
		if capture.output != io['output']:
			print('Output does not match!')
			for a, b in itertools.zip_longest(capture.output, io['output'], fillvalue = ''):
				s1 = a.rjust(30)
				s2 = b.ljust(30)
				if a == b:
					print(s1, '   ', s2)
				else:
					print(s1, '---', s2)
			return False
	return True

if __name__ == '__main__':		

	print('Running unit tests...')

	for i in open_relative('tests.txt'):
		n = i.strip()
		if not run_test(n):
			break
	else:
		print('Done!')