from vivarium.data.datatype import DataType

class String(DataType):

	def __init__(self, value = ''):
		assert isinstance(value, str)
		self.value = value

	def __int__(self):
		return int(self.value)

	def __str__(self):
		return self.value

	def copy(self):
		return String(self.value)

	def __add__(self, other):
		if type(other) is not String:
			raise Exception('Attempted to add a string to something that was not a string')
		return String(self.value + other.value)

	def __len__(self):
		return len(self.value)

	def __bool__(self):
		return len(self.value) > 0

	def __repr__(self):
		return self.value
