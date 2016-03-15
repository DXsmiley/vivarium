def assert_datatype(value):
	if not isinstance(value, DataType):
		raise Exception("{} (of type {}) is not a DataType".format(str(value), type(value)))

class DataType:
	
	def copy(self):
		return self

	def __int__(self):
		raise Exception('{} does not support conversion to an integer.'.format(type(self)))
