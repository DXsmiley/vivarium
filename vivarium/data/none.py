from vivarium.data.datatype import DataType

class _NoneType_(DataType):

	def __call__(self):
		return self

	def __bool__(self):
		return False

	def __str__(self):
		return 'None' 

NoneType = _NoneType_()
