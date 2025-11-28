def test_func(spam, eggs):
	foo = 10
	return spam * eggs + foo

def another(spam, eggs):
	foo = 10
	return spam - eggs - foo

result = test_func(11, 22)

another(result, 44)


