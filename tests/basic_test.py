import unittest
import sys
sys.path.append('../src/')

# All the functions and class we want to test
import ws_nbc, ner_model

class Testing(unittest.TestCase):

    def test_0_get_unique_results(self):
        a = {'NAME': ['Kevin', 'Joe'], 'ORGANIZATION': ['Apple','Amazon'], 'LOCATION': ['Canada', 'USA']}
        test = 'My name is Kevin and my friends name is Joe.  I work for Apple and my friend works for Amazon.  I live in Canada and my friend lives in USA'
        model = ner_model.model()
        ner_results = model.ner(test)
        b = ner_model.get_unique_results(ner_results)
        self.assertEqual(a,b)
        

if __name__ == '__main__':
    unittest.main()