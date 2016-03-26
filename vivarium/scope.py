import vivarium.data.store
import vivarium.data.none
import vivarium.data.function
import vivarium.data.datatype

class Scope:
	"""Stores program state. Includes variables and not much else."""

	def __init__(self, superscope = None):
		"""Create a scope.

		Things not found in this scope are searched for in the superscope.
		This happens recursively."""
		self.values = {}
		self.superscope = superscope

	def get(self, name):
		"""Returns the Store containing the variable called `name`.

		Searches in order to obtain the value of the variable."""
		if name in self.values:
			return self.values[name]
		if self.superscope is None:
			raise Exception('no variable ' + str(name))
		return self.superscope.get(name)

	def set(self, name, is_first = True):
		"""Returns the Store containing the variable called `name`.

		Searches in order to set the value of the variable.
		If the variable doesn't exists within the current scope,
		or any superscope, it will be created in the current scope.

		Arguments
		name -- The name of the variable.
		is_first -- Internal use only."""
		result = None
		# If we have the variable, set it
		if name in self.values:
			result = self.values[name]
		# Look for it in the superscope
		if self.superscope is not None:
			result = self.superscope.set(name, is_first = False)
		# If variable was not found in the superscope, and we are the immidiate scope,
		# create the variable
		if result is None and is_first:
			result = vivarium.data.store.Store(vivarium.data.none.NoneType)
			self.values[name] = result
		return result

	def lockdown(self):
		"""Makes all the values contained within the scope read-only"""
		for k, v in self.values.items():
			v.readonly = True

	def unset(self, name):
		"""Remove a variable. Doesn't search superscopes.
		Usefull when modifying the global scope given by global_scope(), if you don't
		want the program to be able to `print` to the console or something."""
		del self.values[name]

	def __repr__(self):
		l = ['{}: {}'.format(k, v) for k, v in self.values.items()]
		return '{' + ', '.join(l) + '}'

def print_function(*args):
	print(*args)

def int_function(v):
	try:
		return vivarium.data.numeric.Integer(int(v))
	except Exception:
		msg = 'Cannot convert "{}" to an integer'.format(v)
		raise Exception(msg)

def str_function(v):
	return vivarium.data.string.String(str(v))

def input_function(prompt = ''):
	return vivarium.data.string.String(input(str(prompt)))

def max_function(*args):
	return vivarium.data.numeric.Integer(max(int(i) for i in args))

def min_function(*args):
	return vivarium.data.numeric.Integer(min(int(i) for i in args))

def global_scope():
	"""Returns a pre-made 'global' scope containing some basic functions.

	Note that these are writeable, so you might wanted to called `lockdown` on it
	fore it's passed to the program."""
	globs = Scope()
	globs.set('print').set(vivarium.data.function.FunctionBuiltin(print_function))
	globs.set('input').set(vivarium.data.function.FunctionBuiltin(input_function))
	globs.set('int').set(vivarium.data.function.FunctionBuiltin(int_function))
	globs.set('str').set(vivarium.data.function.FunctionBuiltin(str_function))
	globs.set('max').set(vivarium.data.function.FunctionBuiltin(max_function))
	globs.set('min').set(vivarium.data.function.FunctionBuiltin(min_function))
	return globs