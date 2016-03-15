from vivarium.data.datatype import DataType
from vivarium.data.boolean import Boolean
from vivarium.data.none import NoneType

def smart_numeric(value):
	if type(value) is int:
		return Integer(value)
	if type(value) is float:
		return Float(value)
	raise TypeError("{} is not numeric".format(value))

class Numeric(DataType):

	def __init__(self, value = 0):
		assert isinstance(value, int) or isinstance(value, float)
		self.value = value

	def copy(self):
		return type(self)(self.value)

	def __add__(self, other):
		if not isinstance(other, Numeric):
			raise TypeError('Attempted to add an number to something that was not an number.')
		return smart_numeric(self.value + other.value)

	def __sub__(self, other):
		if not isinstance(other, Numeric):
			raise TypeError('Attempted to subtract a non-number from an number.')
		return smart_numeric(self.value - other.value)

	def __mul__(self, other):
		if not isinstance(other, Numeric):
			raise TypeError('Attempted multiply an number by a non-number.')
		return smart_numeric(self.value * other.value)

	def __truediv__(self, other):
		if not isinstance(other, Numeric):
			raise TypeError('Attempted divide an number by a non-number.')
		return Float(self.value / other.value)

	def __floordiv__(self, other):
		if not isinstance(other, Numeric):
			raise TypeError('Attempted (floor) divide an number by a non-number.')
		return smart_numeric(self.value // other.value)

	def __mod__(self, other):
		if not isinstance(other, Numeric):
			raise TypeError('Attempted (modulus) divide an number by a non-number.')
		return smart_numeric(self.value % other.value)

	def __pow__(self, other):
		if not isinstance(other, Numeric):
			raise TypeError('Attempted (modulus) divide an number by a non-number.')
		return smart_numeric(self.value ** other.value)

	def __eq__(self, other):
		if other is None or other is NoneType:
			return False
		if not isinstance(other, Numeric):
			raise TypeError('Comparison of numbers and non-numbers is not allowed.')
		return Boolean(self.value == other.value)

	def __ne__(self, other):
		if other is None or other is NoneType:
			return True
		if not isinstance(other, Numeric):
			raise TypeError('Comparison of numbers and non-numbers is not allowed.')
		return Boolean(self.value != other.value)

	def __lt__(self, other):
		if not isinstance(other, Numeric):
			raise TypeError('Comparison of numbers and non-numbers is not allowed.')
		return Boolean(self.value < other.value)

	def __gt__(self, other):
		if not isinstance(other, Numeric):
			raise TypeError('Comparison of numbers and non-numbers is not allowed.')
		return Boolean(self.value > other.value)

	def __le__(self, other):
		if not isinstance(other, Numeric):
			raise TypeError('Comparison of numbers and non-numbers is not allowed.')
		return Boolean(self.value <= other.value)

	def __ge__(self, other):
		if not isinstance(other, Numeric):
			raise TypeError('Comparison of numbers and non-numbers is not allowed.')
		return Boolean(self.value >= other.value)

	def __int__(self):
		return int(self.value)

	def __float__(self):
		return float(self.value)

	def __str__(self):
		return str(self.value)

	def __bool__(self):
		return (self.value != 0)

	def __repr__(self):
		return str(self.value)

class Integer(Numeric):
	pass

class Float(Numeric):
	pass
