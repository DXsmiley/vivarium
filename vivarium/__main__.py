if __name__ == '__main__':

	import vivarium.transform
	import vivarium.scope
	import vivarium.data.function
	import sys

	def display_syntax_error(e, show_line_nums = True):
		text = e.text
		off = e.offset
		if show_line_nums:
			print('Syntax Error on line {}:'.format(e.lineno))
		else:
			print('Syntax Error')
		print(text[:-1])
		print((' ' * off) + '^')

	def proc_code(code, the_scope, show_line_nums = True):
		result = None
		try:
			bytecode = vivarium.transform.transform(code)
		except SyntaxError as e:
			display_syntax_error(e, show_line_nums)
			return None
		try:
			result = bytecode.evaluate(the_scope)
		except Exception as e:
			print('Runtime Error')
			print(str(e))
		return result

	def help_func(topic = ''):
		topic = str(topic)
		if not topic:
			print('Help has not been implemented.')
		else:
			print('Help on \'{}\' has not been implemented.'.format(topic))

	if len(sys.argv) == 1:
		print('Vivarium development version.')
		globs = vivarium.scope.global_scope()
		globs.set('help').set(vivarium.data.function.FunctionBuiltin(help_func))
		globs.lockdown()
		# print(globs)
		the_scope = vivarium.scope.Scope(globs)
		while True:
			code = input('>>> ')
			if code in ('exit', 'exit()', 'quit', 'quit()'):
				break
			elif code in ('help'):
				print("Type 'help()' for general help, or 'help(topic)' for help on a particular topic.")
			else:
				r = proc_code(code, the_scope, False)
				if r != None:
					print(r)
	else:
		for i in sys.argv[1:]:
			the_scope = vivarium.scope.Scope(vivarium.scope.global_scope())
			with open(i) as f:
				code = f.read()
			proc_code(code, the_scope)