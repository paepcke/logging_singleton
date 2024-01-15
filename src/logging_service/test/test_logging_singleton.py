'''
Created on Jan 15, 2024

@author: paepcke
'''
from enum import Enum
from logging_service.logging_service import LoggingService
import io
import logging
import tempfile
import unittest

TEST_ALL = True
#TEST_ALL = False

class Stream(Enum):
    STDOUT = 0
    STDERR = 1

class SingletonLoggerTest(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    # ------------------- Tests -------------

    #------------------------------------
    # test_single_instance
    #-------------------
    
    @unittest.skipIf(TEST_ALL != True, 'skipping temporarily')
    def test_single_instance(self):
        log1 = LoggingService()
        log2 = LoggingService()
        self.assertEqual(id(log1), id(log2))
    
    #------------------------------------
    # test_log_level
    #-------------------
    
    @unittest.skipIf(TEST_ALL != True, 'skipping temporarily')
    def test_log_level(self):
        
        log = LoggingService()
        log.logging_level = logging.DEBUG
        
        # All above DEBUG should print:
        with self.assertPrints("Debug test",log=log): 
            log.debug('Debug test')
            
        with self.assertPrints("Info test",log=log):
            log.info('Info test')
        
        with self.assertPrints("Warn test",log=log):
            log.warn('Warn test')
        
        with self.assertPrints("Error test",log=log):
            log.err('Error test')
        
        with self.assertPrints("Critical test",log=log):
            log.critical('Critical test')
        
        # Change logging level:
        log.logging_level = logging.ERROR
        # Now only error and critical should print anything:
        with self.assertPrints("Error test",log=log):
            log.err('Error test')
        
        with self.assertPrints("Critical test",log=log):
            log.critical('Critical test')
        
        # ... Info should not show:
        with self.assertPrints("",log=log, trailing_nl=False):
            log.info('Info test')
        
    #------------------------------------
    # test_level_names
    #-------------------
    
    @unittest.skipIf(TEST_ALL != True, 'skipping temporarily')
    def test_level_names(self):

        log = LoggingService()
        log.logging_level = logging.DEBUG
        
        self.assertDictEqual(log.logging_level, 
                             {'name' : 'DEBUG', 'number' : logging.DEBUG})

    #------------------------------------
    # test_tee_to_console
    #-------------------
    
    #****@unittest.skipIf(TEST_ALL != True, 'skipping temporarily')
    def test_tee_to_console(self):
        
        log = LoggingService(tee_to_console=True)
        log.logging_level = logging.INFO
        
        

        
    #------------------------------------
    # test_file_logging
    #-------------------
    
    @unittest.skipIf(TEST_ALL != True, 'skipping temporarily')
    def test_file_logging(self):
        
        # Test to file, and then read back:
        #  Written  :  'test_logging_...INFO: This is a log file test.'
        #  Read back: ['test_logging_...INFO: This is a log file test.\n']
        
        with tempfile.NamedTemporaryFile(delete=True) as fd:
            log = LoggingService(logfile=fd.name)
            msg = "This is a log file test."
            log.info(msg)
            with open(fd.name, 'r') as fd_read:
                content  = fd_read.readlines()[0]
                self.assertTrue(content.endswith(f"{msg}\n"))

    #------------------------------------
    # test_logging_level_adjustment
    #-------------------
    
    @unittest.skipIf(TEST_ALL != True, 'skipping temporarily')
    def test_logging_level_adjustment(self):
        
        log1 = LoggingService()
        log1.logging_level = logging.INFO
        expected1 = {'name' : 'INFO', 'number' : 20}
        self.assertDictEqual(log1.logging_level, expected1)
        
        # Init won't run!!! So, no setting to DEBUG; logging level
        # remains at INFO:
        log2 = LoggingService(logging_level=logging.DEBUG)
        self.assertDictEqual(log1.logging_level, expected1)
        self.assertDictEqual(log2.logging_level, expected1)
        
        log2.logging_level = logging.DEBUG
        expected2 = {'name' : 'DEBUG', 'number' : 10}
        self.assertDictEqual(log1.logging_level, expected2)
        self.assertDictEqual(log2.logging_level, expected2)
        
    # ---------------- Stdout Redirects -------
    
    #------------------------------------
    # assertPrints
    #-------------------

    # As a bonus, this syntactical sugar becomes possible:
    def assertPrints(self, *expected_output, 
                     trailing_nl=True,
                     log=None):
        '''
        Version of assertStdout that takes multiple
        lines of expected output. Usage:
        
	         with self.assertPrints("test1", "test2"):
	             print("test1")
	             print("test2")        
	         
        :param *expected_output: any number of expected strings
        :type *expected_output: str
        :param stream: which output stream to monitor
        :type stream: Stream
        :raise AssertionError
        '''
        expected_output = "\n".join(expected_output) +\
            "\n" if trailing_nl else ''
        return _AssertStdoutContext(self, expected_output, log=log)
    
# ---------------- Stdout Redirect Context Manager ---------    

class _AssertStdoutContext:
    '''
    Context manager that temporarily re-assignes
    stdout into a StringIO. On exit, compares
    captured print output with given expected value.
    
    credit: @NichtJens 
       https://stackoverflow.com/questions/33767627/python-write-unittest-for-console-print
    '''

    def __init__(self, testcase, expected, log=None):
        '''
        
        :param testcase: instance test case
        :type testcase: unittest.TestCase
        :param expected: expected captured print string(s)
        :type expected: str
        '''
        self.testcase = testcase
        self.expected = expected
        self.captured = io.StringIO()
        self.log      = log

    def __enter__(self):
        '''
        Context entry: monitor either stdout or
        stderr.
        
        :param stream: which output stream to monitor
        :type stream: Stream
        '''
        self.orig_stream = self.log.handlers[0].stream
        self.log.handlers[0].setStream(self.captured)
        return self

    def __exit__(self, _exc_type, _exc_value, _tb):
        captured = self.captured.getvalue()
        self.log.handlers[0].setStream(self.orig_stream)
        
        if len(self.expected) == 0:
            self.testcase.assertTrue(len(captured) == 0)
        else:
            self.testcase.assertTrue(captured.endswith(self.expected))

# ------------------------- Main ------------
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()