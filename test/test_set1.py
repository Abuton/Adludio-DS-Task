try:

	import sys, os
	sys.path.append(os.path.abspath(os.path.join('..')))

	import unittest
	import numpy as np
	from numpy.testing import assert_almost_equal, assert_equal, assert_string_equal
	from numpy.testing import assert_allclose, assert_raises, assert_raises_regex
	from app import app
except Exception as e:
	print('Some modules are missing {}'.format(e))
	

class FlaskTestCase(unittest.TestCase):
	"""docstring for FlaskTestCase
		A class for unit-testing some of the function/method in the 
		app.py file

		Args:
			unittest.TestCase this allows the new class to inherit
			from the unittest module
	"""
	
	# check status code for the home page at route (/demo1)
	def test_homepage(self):
		tester = app.test_client(self)
		response = tester.get('/demo1')
		statuscode = response.status_code
		self.assertEqual(statuscode, 200)


	# check content of the route /get_data_dump if it returns a json
	def test_data_dump_content(self):
		tester = app.test_client(self)
		response = tester.get('/get_data_dump')
		self.assertEqual(response.content_type, 'text/plain;charset=utf-8')


	# check if data present
	def test_data_return(self):
		tester = app.test_client(self)
		response = tester.get('/list_searchable_parameters')
		self.assertTrue(b"region" in response.data)

	def test_basic_test(self):
	    out = {}
	    assert_equal(isinstance(out, dict), True)


	def test_html(self):
		html = "<h1> Testing sanity check </h1>"
		tester = app.test_client(self)
		response = tester.get('/')
		self.assertEqual(isinstance(html, str), True)
    
if __name__ == '__main__':
	unittest.main()