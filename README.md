# Vivarium

Vivarium is an implementation of python, written in python. It is designed to restrict the environment of any executed code.

## Installation

	git clone this_repo

## Shell

The vivarium shell is very similar to the default python one, but will fewer features.

	python -m vivarium

## Quickstart

	import vivarium
	untrusted_code = input('Enter the code: ')
	output = vivarium.easy.run(untristed_code)
	print(output)

The `vivarium.easy` module contains some helper functions to effortlessly execute code.
The `vivarium.easy.run` function takes the code as a string, and returns the (`print`ed) output as a list of strings.
