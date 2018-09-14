project('rang_test', 'cpp', version : '3.1.0',
		default_options : ['cpp_std=c++11'])

rang = dependency('rang')

visualTest = executable('visualTest', 'visualTest.cpp', dependencies : rang)
test('visualTest', visualTest)
