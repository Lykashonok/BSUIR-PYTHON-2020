import unittest
import json # to check wether jsonByVlad works correctly
import time # to check memoization speed

import sys
sys.path.append('../')

from vectorByVlad.core import VectorByVlad
from jsonByVlad.core import to_json, from_json
from memoizationByVlad.core import factorial, fibonacci
from externalSortByVlad.core import external_sort, quick_sort

class TestJson(unittest.TestCase):
    def test_from_json(self):
        self.assertEqual(from_json('{"name" :null,"age":30,"city":"New York''","cards":[".1234\","4321",[]]}'), json.loads('{"name" :null,"age":30,"city":"New York''","cards":[".1234\","4321",[]]}'))
        self.assertEqual(from_json('{"bool":false,"bool2":true,"string":"string","array":[{"obj":{}},"4321"]}'), json.loads('{"bool":false,"bool2":true,"string":"string","array":[{"obj":{}},"4321"]}'))
        self.assertRaises(ValueError, from_json, '{"bool":,"bool2":,"string":"string",:[{"obj":{}},"4321"]}')
        self.assertRaises(ValueError, from_json, '{:[{"obj":{}},"4321" 2]}')
        self.assertRaises(ValueError, from_json, '{"qwer":[{"obj":{}},"4321",]}')
        self.assertRaises(ValueError, from_json, '{"qwer":[{"obj":{}},"4321",{2: ''}]}')
        
    def test_to_json(self):
        obj = {"name":None,"age":30.2,"bool":False,"bool2":True,"tmp":[2,3.0],"city":"New York","empty":{},"cards":["1234","4321","qwe",False,True,None,[],{}]}
        self.assertEqual(to_json(obj),json.dumps(obj))
    
    def test_vbv_operations(self):
        vector = VectorByVlad([1, 2, 3])
        self.assertEqual(str(vector), 'VBV(1, 2, 3)')
        self.assertTrue(-vector or VectorByVlad([0]) == True and vector != VectorByVlad([0]) and not vector == '2')
        self.assertEqual(vector, vector)
        self.assertEqual(bool(vector), True)
        self.assertNotEqual(vector, -vector)
        self.assertEqual(vector+vector-vector, vector)
        self.assertEqual(abs(VectorByVlad([0,0,0])), 0)
        self.assertEqual(VectorByVlad([0])[0], VectorByVlad([1,2]) * VectorByVlad([0,0]) * 5)
        if vector != 2: vector[0] = 2 * vector[0]
        self.assertEqual(vector[0], 2)
        self.assertFalse(VectorByVlad([]) == 0)
        vector += vector
        vector -= VectorByVlad([0,0,0])
        vector *= 2
        vector = vector * 2
        self.assertEqual(vector[0], 16) 

    def test_vbv_raises(self):
        vector = VectorByVlad([1, 2, 3])
        self.assertRaises(ValueError, lambda: vector[20])

    def test_external_sort(self):
        def is_sorted(file):
            with open(file) as file_to_output:
                number_prev = file_to_output.readline()
                number_new = number_prev
                while number_new:
                    number_new = file_to_output.readline()
                    if number_new and int(number_new) < int(number_prev): return False
                return True
        #if buffer will be bigger than file, part of code wont be covered, cause it wont create more than 1 file
        external_sort(FILE_TO_SORT="numbers.txt", FILE_TO_OUTPUT="output.txt", BUFFER_SIZE=2000)
        self.assertTrue(is_sorted("output.txt"))
        self.assertEqual(quick_sort([2,3,1,0,-2], compare_function=lambda a, b: a > b, reversed=True), [3,2,1,0,-2])

    def test_external_sort_raises(self):
        with self.assertRaises(ValueError):
            external_sort("output.txt", "output.txt")
    
    def test_memoization(self):
        
        # calculate time for first execution
        time_passed_first = time.time()
        self.assertEqual(fibonacci(30), 832040)
        time_passed_first = (time.time() - time_passed_first)
        # calculate time for second
        time_passed_second = time.time()
        self.assertEqual(fibonacci(30), 832040)
        time_passed_second = (time.time() - time_passed_second)
        # see if second time less more than 2 times than first, 
        # it means that second execution was rather faster
        # cause there wasnt any computations
        self.assertTrue(time_passed_second / time_passed_first < 0.5)

        time_passed_first = time.time()
        self.assertEqual(factorial(6), 720)
        time_passed_first = (time.time() - time_passed_first)
        time_passed_second = time.time()
        self.assertEqual(factorial(6), 720)
        time_passed_second = (time.time() - time_passed_second)
        self.assertTrue(time_passed_second / time_passed_first < 0.5)

    def test_memoization_raise(self):
        self.assertRaises(ValueError,fibonacci, -20)
        self.assertRaises(ValueError,factorial, -1)
            

# def main():
#     unittest.main()

# to test with coverage type
# coverage run testModuleByVlad.py && coverage report
if __name__ == '__main__':
    unittest.main()