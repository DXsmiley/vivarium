from vivarium.data.datatype import DataType
import vivarium.signal

class Function(DataType):
	"""A callable function."""

	def __init__(self, argument_names, block, superscope):
		"""Construct a callable function

		Arguments:
		argument_names -- The names of the arguments. Pass as a list of strings.
		block -- The statements contained within the function. Usually a vivarium.core.Statements object.
		superscope -- The scope from which the function was created.
		"""
		self.argument_names = argument_names
		self.block = block
		self.superscope = superscope

	def call(self, arguments):
		"""Execute the function and return the result.

		Arguments:
		arguments -- The values passed to the function. A list of DataTypes.
		"""
		assert len(self.argument_names) == len(arguments)
		scope = vivarium.scope.Scope()
		for name, value in zip(self.argument_names, arguments):
			scope.set(name).set(value)
		# Setting the superscope afterwards avoids arguments
		# overwritting variables in the superscope
		# Might add a warning on this or something
		scope.superscope = self.superscope
		result = None
		try:
			self.block.evaluate(scope)
		except vivarium.signal.ReturnSignal as signal:
			result = signal.data
		return result

class FunctionBuiltin(DataType):
	"""Used as a way to wrap a function implemented in normal python."""

	def __init__(self, func):
		"""Create the builtin"""
		self.func = func

	def call(self, arguments):
		"""Call the builtin function. Unlike normal functions (currently), this may be varidic."""
		return self.func(*arguments)

	def __repr__(self):
		return 'builtin function'