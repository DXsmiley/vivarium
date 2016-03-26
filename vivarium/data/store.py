from vivarium.data.datatype import assert_datatype

class Store:
	"""Stores a single datum."""

	def __init__(self, value, readonly = False):
		"""Create a store.

		Arguments:
		value -- The initial value. Must be derived form DataType.
		readonly -- Whether the store is read-only. Defaults to False.
		"""
		assert_datatype(value)
		self.value = value
		self.readonly = readonly

	def get(self):
		"""Retreive the stored value"""
		return self.value

	def set(self, value):
		"""Set the stored value. Must be a DataType."""
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
