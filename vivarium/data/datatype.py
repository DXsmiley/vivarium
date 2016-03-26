def assert_datatype(value):
	"""Ensure that the object as a vivarium DataType"""
	if not isinstance(value, DataType):
		raise Exception("{} (of type {}) is not a DataType".format(str(value), type(value)))

class DataType:
	"""Base class for vivarium data types.

	All data types that vivarium can handle should be derived from this."""
	
	def copy(self):
		"""'Duplicate' the object.

		In most cases, this just returns a reference to itself (as when copying objects).
		Primitive types, such as ints and strings override this."""
		return self

	def __int__(self):
		raise Exception('{} does not support conversion to an integer.'.format(type(self)))
