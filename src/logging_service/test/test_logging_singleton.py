'''
Created on Jan 15, 2024

@author: paepcke
'''
from enum import Enum
from logging_service.logging_service import LoggingLevel, LoggingService
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
    # test_log_level_int_levels
    #-------------------
    
    @unittest.skipIf(TEST_ALL != True, 'skipping temporarily')
    def test_log_level_int_levels(self):
        
        # Test whether passing a log level 
        # to initializer sets the level:
        log = LoggingService()
        log.setLevel(logging.DEBUG) # 10
        #**********
        print(f"logging_level['number']: {log.logging_level['number']}")
        print(f"logging.DEBUG: {logging.DEBUG}")
        #**********
        self.assertEqual(log.logging_level['number'], logging.DEBUG)
    
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
    # test_log_level_enum_levels
    #-------------------
    
    @unittest.skipIf(TEST_ALL != True, 'skipping temporarily')
    def test_log_leve_enum_levelsl(self):
        
        # Test whether passing a log level 
        # to initializer sets the level:
        log = LoggingService(logging_level=LoggingLevel.DEBUG)
        self.assertEqual(log.logging_level['number'], LoggingLevel.DEBUG.value)
    
        log = LoggingService()
        log.logging_level = LoggingLevel.DEBUG
    
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
        log.logging_level = LoggingLevel.ERROR
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
    
    @unittest.skipIf(TEST_ALL != True, 'skipping temporarily')
    def test_tee_to_console(self):
    
        with tempfile.NamedTemporaryFile(delete=True) as fd:
    
            log = LoggingService(logging_level=logging.INFO,
                                 tee_to_console=True, 
                                 force=True,
                                 logfile=fd.name)
    
            msg = "This is log file TEE to console test."
            with self.assertPrints(msg, log=log):
                log.info(msg)
            fd.seek(0)
            with open(fd.name, 'r') as fd_read:
                lines  = fd_read.readlines()
                self.assertEqual(len(lines), 1, f"Number of lines in file: {len(lines)}")
                content = lines[0]
                self.assertTrue(content.endswith(f"{msg}\n"))

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
        
    #------------------------------------
    # test_new_instance_forcing
    #-------------------
    
    @unittest.skipIf(TEST_ALL != True, 'skipping temporarily')
    def test_new_instance_forcing(self):
        
        log1 = LoggingService()
        log1.logging_level = logging.DEBUG
        
        # Now force a new instance, initilizing logging level:
        log2 = LoggingService(logging_level=logging.INFO, force=True)
        self.assertEqual(log2.logging_level['name'], 'INFO')
        
        # But log1 is still DEBUG:
        self.assertEqual(log1.logging_level['name'], 'DEBUG')
        
    #------------------------------------
    # test_logger_name
    #-------------------
    
    @unittest.skipIf(TEST_ALL != True, 'skipping temporarily')
    def test_logger_name(self):
        
        log = LoggingService(logger_name='MyName', force=True)
        log.info("This is a test")
        
    #------------------------------------
    # test_msg_identifier
    #-------------------
    
    @unittest.skipIf(TEST_ALL != True, 'skipping temporarily')
    def test_msg_identifier(self):
    
        log = LoggingService(msg_identifier='My module', force=True)
        msg = "This is mod name test"
        tst_func = lambda s, b: s.startswith(b)
        with self.assertPrints('My module', 
                               log=log, 
                               tst_func=tst_func, 
                               trailing_nl=False):
            log.info(msg)
        
    # ---------------- Stdout Redirects -------
    
    #------------------------------------
    # assertPrints
    #-------------------

    # As a bonus, this syntactical sugar becomes possible:
    def assertPrints(self, *expected_output, 
                     trailing_nl=True,
                     log=None,
                     tst_func=None):
        '''
        Version of assertStdout that takes multiple
        lines of expected output. Usage:
        
	         with self.assertPrints("test1", "test2"):
	             print("test1")
	             print("test2")        
	         
        :param *expected_output: any number of expected strings
        :type *expected_output: str
        :param trailing_nl: whether or not to expect an nl
            after the expected output
        :type trailing_nl: bool
        :param log: LoggingService instance
        :type log: LoggingService
        :param tst_func: function that returns True/False when
            comparing expected to actual. The function will be
            called with two strings.
        :type tst_func: callable
        :raise AssertionError
        '''
        if trailing_nl:
            expected_output = "\n".join(expected_output) + '\n'
        else:
            expected_output = "\n".join(expected_output)
        return _AssertStdoutContext(self, expected_output, log=log, tst_func=tst_func)
    
# ---------------- Stdout Redirect Context Manager ---------    

class _AssertStdoutContext:
    '''
    Context manager that temporarily re-assignes
    stdout into a StringIO. On exit, compares
    captured print output with given expected value.
    
    credit: @NichtJens 
       https://stackoverflow.com/questions/33767627/python-write-unittest-for-console-print
    '''

    def __init__(self, testcase, expected, log=None, tst_func=None):
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
        if tst_func is None:
            self.tst_func = lambda s, e: s.endswith(e)
        else:
            self.tst_func = tst_func

    def __enter__(self):
        '''
        Context entry: monitor either stdout or
        stderr.
        
        :param stream: which output stream to monitor
        :type stream: Stream
        '''
        self.handler_to_mod = None
        for handler in self.log.handlers:
            if type(handler) == logging.StreamHandler:
                self.handler_to_mod = handler
                break
        if self.handler_to_mod is None:
            raise RuntimeError("Log does not contain a console stream handler")
        
        self.orig_stream = self.handler_to_mod.stream
        self.handler_to_mod.setStream(self.captured)
        return self

    def __exit__(self, _exc_type, _exc_value, _tb):
        captured = self.captured.getvalue()
        self.handler_to_mod.setStream(self.orig_stream)
        
        if len(self.expected) == 0:
            self.testcase.assertTrue(len(captured) == 0)
        else:
            self.testcase.assertTrue(self.tst_func(captured, self.expected),
                                     f"got '{captured}';  exp: '{self.expected}'"
                                     )

# ------------------------- Main ------------
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()