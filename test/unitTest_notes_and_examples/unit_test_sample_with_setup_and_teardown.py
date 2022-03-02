'''
Created on 10 Sep 2021

@author: hsth
'''
import unittest


class Test(unittest.TestCase):

    def set_up(self):
        # If the set_up method raises an exception while the test is running, 
        # the framework will consider the test to have suffered an error, 
        # and the runTest (or test_X_Name) method will not be executed.
        pass


    def tear_down(self):
        # If set_up succeeded, the tear_down method will be 
        # run regardless of whether or not runTest (or test_X_Name) succeeded.
        pass


    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()