from vivarium.data.datatype import assert_datatype

class Store:

	def __init__(self, value, readonly = False):
		assert_datatype(value)
		self.value = value
		self.readonly = readonly

	def get(self):
		return self.value

	def set(self, value):
		assert_datatype(value)
		if self.readonly:
			raise Exception('Cannot write to readonly data store ' + str(self))
		if type(value) is Store:
			value = value.get()
		self.value = value.copy()

	def __repr__(self):
		if self.readonly:
			return 'READONLY(' + str(self.value) + ')'
		return 'STORE(' + str(self.value) + ')'
