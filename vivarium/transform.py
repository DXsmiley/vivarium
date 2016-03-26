"""Used to convert a string into an executable structure.

Calling `transform("code as a string")` will probably be enough."""

import vivarium.core
import vivarium.data.string
import vivarium.data.numeric
import vivarium.data.none
import vivarium.data.boolean
import ast

def t_module(node):
	l = [transform(i) for i in node.body]
	return vivarium.core.Statements(l)

def t_name_constant(node):
	if node.value is None:
		return vivarium.core.Constant(vivarium.data.none.NoneType)
	else:
		return vivarium.core.Constant(vivarium.data.boolean.Boolean(node.value))

def t_list(node):
	assert type(node.ctx) is ast.Load
	return vivarium.core.List(list(transform(i) for i in node.elts))

def t_tuple(node):
	assert type(node.ctx) is ast.Load
	return vivarium.data.Tuple(list(transform(i) for i in node.elts))

def t_assign(node):
	assert len(node.targets) == 1
	expression = transform(node.value)
	target = transform(node.targets[0])
	return vivarium.core.SetStatement(target, expression)

def t_num(node):
	return vivarium.core.Constant(vivarium.data.numeric.smart_numeric(node.n))

def t_str(node):
	return vivarium.core.Constant(vivarium.data.string.String(node.s))

def t_name(node):
	if type(node.ctx) is ast.Store:
		return vivarium.core.VariableReference(node.id)
	else:
		return vivarium.core.Variable(node.id)

def t_call(node):
	func = transform(node.func)
	args = vivarium.core.ArgumentList()
	args.add_multiple(list(transform(i) for i in node.args))
	return vivarium.core.FunctionCall(func, args)

def t_expr(node):
	return transform(node.value)

def t_binop(node):
	t = type(node.op)
	l = transform(node.left)
	r = transform(node.right)
	if t is ast.Add:
		return vivarium.core.BinOp(l, r, '+')
	if t is ast.Sub:
		return vivarium.core.BinOp(l, r, '-')
	if t is ast.Mult:
		return vivarium.core.BinOp(l, r, '*')
	if t is ast.Div:
		return vivarium.core.BinOp(l, r, '/')
	if t is ast.FloorDiv:
		return vivarium.core.BinOp(l, r, '//')
	if t is ast.Mod:
		return vivarium.core.BinOp(l, r, '%')
	if t is ast.Pow:
		return vivarium.core.BinOp(l, r, '**')
	raise Exception('Unable to process binary operator of type ' + str(t))

def t_comp_op(node):
	t = type(node)
	r = {
		ast.Eq:    '==',
		ast.NotEq: '!=',
		ast.Lt:    '<',
		ast.LtE:   '<=',
		ast.Gt:    '>',
		ast.GtE:   '>=',
	}.get(t)
	if not r:
		raise Exception('Unknown comparitor ' + str(t))
	return r

def t_compare(node):
	assert len(node.ops) == 1
	assert len(node.comparators) == 1
	l = transform(node.left)
	r = transform(node.comparators[0])
	c = t_comp_op(node.ops[0])
	return vivarium.core.Comparison(l, c, r)

def t_if(node):
	c = transform(node.test)
	b = transform(node.body)
	e = transform(node.orelse)
	return vivarium.core.IfBranch(c, b, e)

def t_statement_list(lst):
	s = vivarium.core.Statements([])
	for i in lst:
		s.add(transform(i))
	return s

def t_while(node):
	assert node.orelse == []
	condition = transform(node.test)
	body = transform(node.body)
	return vivarium.core.WhileLoop(condition, body)

def t_function_def(node):
	name = node.name
	args = transform(node.args)
	body = transform(node.body)
	return vivarium.core.FunctionDefinition(name, args, body)

def t_arguments(node):
	arg_names = []
	for i in node.args:
		arg_names.append(i.arg)
	return arg_names

def t_return(node):
	return vivarium.core.Return(transform(node.value))

def transform(node):
	t = type(node)
	if t is str:
		return transform(ast.parse(node))
	if t is list:
		return t_statement_list(node)
	if t is ast.NameConstant:
		return t_name_constant(node)
	if t is ast.List:
		return t_list(node)
	if t is ast.Tuple:
		return t_tuple(node)
	if t is ast.Return:
		return t_return(node)
	if t is ast.Module:
		return t_module(node)
	if t is ast.Assign:
		return t_assign(node)
	if t is ast.Num:
		return t_num(node)
	if t is ast.Str:
		return t_str(node)
	if t is ast.Name:
		return t_name(node)
	if t is ast.Call:
		return t_call(node)
	if t is ast.Expr:
		return t_expr(node)
	if t is ast.BinOp:
		return t_binop(node)
	if t is ast.If:
		return t_if(node)
	if t is ast.Compare:
		return t_compare(node)
	if t is ast.While:
		return t_while(node)
	if t is ast.FunctionDef:
		return t_function_def(node)
	if t is ast.arguments:
		return t_arguments(node)
	raise Exception('Unable to process node of type ' + str(t))