# Vivarium

Vivarium is an implementation of [Python](http://python.org/), written in Python. It is designed to restrict the environment of executed code.

## Installation

	git clone https://github.com/DXsmiley/vivarium.git

## Shell

The vivarium shell is very similar to the default Python one, but with fewer features.

	python -m vivarium

## Quickstart

	import vivarium
	untrusted_code = input('Enter the code: ')
	output = vivarium.easy.run(untrusted_code)
	print(output)

The `vivarium.easy` module contains some helper functions to effortlessly execute code.
The `vivarium.easy.run` function takes the code as a string, and returns the (`print`ed) output as a list of strings.
