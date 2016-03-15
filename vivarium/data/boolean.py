from vivarium.data.datatype import DataType

class Boolean(DataType):

	def __init__(self, value = True):
		self.value = bool(value)

	def copy(self):
		return Boolean(self.value)

	def __int__(self):
		return 1 if self.value else 0

	def __bool__(self):
		return self.value

	def __str__(self):
		return 'True' if self.value else 'False'
