from vivarium.data.datatype import DataType
import vivarium.signal

class Function(DataType):

	def __init__(self, argument_names, block, superscope):
		self.argument_names = argument_names
		self.block = block
		self.superscope = superscope

	def call(self, arguments):
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

	def __init__(self, func):
		self.func = func

	def call(self, arguments):
		return self.func(*arguments)

	def __repr__(self):
		return 'builtin function'