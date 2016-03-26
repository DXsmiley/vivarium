"""Classes representing Python's syntactic structure.

Most of these implemnt the `evaluate` method."""

import operator
import vivarium.data
import vivarium.signal

def unwrap(d):
	"""Retreives the datum object within a Store.

	Returns the input if it's not a Store."""
	if type(d) is vivarium.data.store.Store:
		return d.get()
	return d

class SetStatement:
	"""Python assignment statement.

	e.g. `x = 7`"""

	def __init__(self, reference, expression):
		"""reference -- A VariableReference object.
		expression -- Any object that implements the evaluate function."""
		self.reference = reference
		self.expression = expression

	def evaluate(self, scope):
		"""Perform the assignment in the given scope. Returns nothing."""
		value = self.expression.evaluate(scope)
		storage = self.reference.evaluate(scope)
		# print(storage, '=', value)
		storage.set(value)

	def __repr__(self):
		return 'SET({}, {})'.format(self.reference, self.expression)

class Variable:
	"""Python variable access.

	e.g. the `y` in `x = y`"""

	def __init__(self, name):
		self.name = name

	def evaluate(self, scope):
		"""Returns the value of the value within the scope."""
		return scope.get(self.name).get()

	def __repr__(self):
		return self.name

class VariableReference:
	"""Python variable reference.

	e.g. the `x` in `x = y`"""

	def __init__(self, name):
		self.name = name

	def evaluate(self, scope):
		"""Returns a reference to the value within the scope."""
		return scope.set(self.name)

	def __repr__(self):
		return '&' + self.name

class Attribute:
	pass

class Statements:
	"""List of Python statements."""

	def __init__(self, statements):
		self.statements = statements

	def add(self, statement):
		self.statements.append(statement)
		return self

	def evaluate(self, scope):
		"""Execute the statements.

		Return the output value of the last one."""
		last_value = None
		for i in self.statements:
			last_value = i.evaluate(scope)
		return last_value

	def __repr__(self):
		return 'STMTS({})'.format(', '.join(str(i) for i in self.statements))

class Constant:
	"""A constant value.

	e.g. `12`"""

	def __init__(self, value):
		self.value = value

	def evaluate(self, scope):
		return self.value

	def __repr__(self):
		return str(self.value)

class List:

	def __init__(self, elements):
		self.elements = elements

	def evaluate(self, scope):
		return list(i.evaluate(scope) for i in self.elements)

	def __repr__(self):
		return '[{}]'.format(', '.join(str(i) for i in self.elements))

class Tuple:

	def __init__(self, elements):
		self.elements = elements

	def evaluate(self, scope):
		return tuple(i.evaluate(scope) for i in self.elements)

	def __repr__(self):
		return '({},)'.format(', '.join(str(i) for i in self.elements))

class IfBranch:
	"""An if (and possible else) statement."""

	def __init__(self, condition, if_block, else_block = None):
		"""Create an if statement.

		Arguments:
		condition -- The test condition. Should be an Expression.
		if_block -- Evaluated if the condition is truthy.
		else_block -- If not None, evaluated if the condition is falsy. Defaults to None."""
		self.condition = condition
		self.if_block = if_block
		self.else_block = else_block

	def evaluate(self, scope):
		if unwrap(self.condition.evaluate(scope)):
			self.if_block.evaluate(scope)
		else:
			if self.else_block != None:
				self.else_block.evaluate(scope)

	def __repr__(self):
		if self.else_block:
			return 'IF({}, {}, {})'.format(self.condition, self.if_block, self.else_block)
		return 'IF({}, {})'.format(self.condition, self.if_block)

class FunctionCall:
	"""A call to a function.

	e.g. `max(1, 2, 3)`"""

	def __init__(self, function_expression, arguments_expression = None):
		"""Create a function call.

		Arguments:
		function_expression -- Should evaluate to something that implements the function `call`.
			This is usually just a VariableReference.
		arguments_expression -- An ArgumentsList. Can be ommitted if no arguments are passed.
		"""
		self.function_expression = function_expression
		self.arguments_expression = arguments_expression if arguments_expression else ArgumentList()

	def evaluate(self, scope):
		"""Execute the function are return the `return`ed value."""
		function = unwrap(self.function_expression.evaluate(scope))
		arguments = self.arguments_expression.evaluate(scope)
		return function.call(arguments)

	def __repr__(self):
		return '{}({})'.format(self.function_expression, self.arguments_expression)

class FunctionDefinition:
	"""The definition of a function.

	e.g. `def f(a, b): return a + b`"""

	def __init__(self, function_name, argument_names, block):
		"""Create a function definition.

		Arguments:
		function_name -- The name of the function, as a string.
		arguments_names -- The names of the arguments. A list of strings.
		block -- The statements within the function."""
		self.function_name = function_name
		self.argument_names = argument_names
		self.block = block

	def evaluate(self, scope):
		new_function = vivarium.data.function.Function(self.argument_names, self.block, scope)
		scope.set(self.function_name).set(new_function)
		return new_function

	def __repr__(self):
		return 'DEF({}; {}; {})'.format(self.function_name, ', '.join(self.argument_names), self.block)

class ArgumentList:
	"""A list of arguments to be evaluated. Used to create a FunctionCall."""
	# The implementation of this is pretty awkward at the moment...

	def __init__(self, first = None):
		self.args = []
		if first:
			self.args = [first]

	def add(self, arg):
		self.args.append(arg)
		return self

	def add_multiple(self, args):
		self.args += args
		return self

	def evaluate(self, scope):
		values = []
		for i in self.args:
			values.append(unwrap(i.evaluate(scope)))
		return values

	def __repr__(self):
		return ', '.join(str(i) for i in self.args)

class Return:
	"""The `return` statement."""

	def __init__(self, expression):
		self.expression = expression

	def evaluate(self, scope):
		data = unwrap(self.expression.evaluate(scope))
		raise vivarium.signal.ReturnSignal(data)

	def __repr__(self):
		return 'RETURN({})'.format(self.expression)

class WhileLoop:
	"""The `while` loop."""

	def __init__(self, condition, block):
		"""Construct a while loop.

		Arguments:
		condition -- An Expression. Loop will run as long as this evaluates truthy.
		block -- The statements within the loop."""
		self.condition = condition
		self.block = block

	def evaluate(self, scope):
		while unwrap(self.condition.evaluate(scope)):
			self.block.evaluate(scope)

	def __repr__(self):
		return 'WHILE({}, {})'.format(self.condition, self.block)

class PrintKeyword:

	def __init__(self, variable):
		self.variable = variable

	def evaluate(self, scope):
		value = self.variable.evaluate(scope)
		# print('PRINT KEYWORD:', value)
		print(value)

	def __repr__(self):
		return 'PRINT({})'.format(self.variable)

class Comparison:

	def __init__(self, left, operator, right):
		self.left = left
		self.right = right
		self.operator = operator

	def evaluate(self, scope):
		l = unwrap(self.left.evaluate(scope))
		r = unwrap(self.right.evaluate(scope))
		if self.operator == '==':
			return l == r
		if self.operator == '!=':
			return l != r
		if self.operator == '<=':
			return l <= r
		if self.operator == '>=':
			return l >= r
		if self.operator == '<':
			return l < r
		if self.operator == '>':
			return l > r

	def __repr__(self):
		return '({} {} {})'.format(self.left, self.operator, self.right)

class BinOp:

	def __init__(self, left, right, op):
		self.left = unwrap(left)
		self.right = unwrap(right)
		self.op_sym = op
		if op == '==':
			self.operator = operator.eq
		elif op == '!':
			self.operator = operator.ne
		elif op == '>':
			self.operator = operator.gt
		elif op == '<':
			self.operator = operator.lt
		elif op == '>=':
			self.operator = operator.ge
		elif op == '<=':
			self.operator = operator.le
		elif op == '-':
			self.operator = operator.sub
		elif op == '+':
			self.operator = operator.add
		elif op == '*':
			self.operator = operator.mul
		elif op == '/':
			self.operator = operator.truediv
		elif op == '//':
			self.operator = operator.floordiv
		elif op == '%':
			self.operator = operator.mod
		elif op == '**':
			self.operator = operator.pow
		else:
			raise Exception('Unknown binary operation ' + op)

	def evaluate(self, scope):
		lv = unwrap(self.left.evaluate(scope))
		rv = unwrap(self.right.evaluate(scope))
		return self.operator(lv, rv)

	def __repr__(self):
		return '({} {} {})'.format(self.left, self.op_syn, self.right)

class Pass:

	def evaluate(self, scope):
		pass

	def __repr__(self):
		return 'PASS'