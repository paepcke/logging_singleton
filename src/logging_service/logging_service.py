'''
Created on Jan 15, 2020

@author: paepcke

Singleton-instance class to share logging among
modules. Rather than the more general logger tree,
this logging facility uses the same logger instance
whenever any module of a program requests a logger.

Usage:

from logging_service.logging_service import LoggingService

Constructor:
            ...
        self.log = LoggingService()
        self.log = LoggingService(logging_level=logging.DEBUG)
        self.log = LoggingService(logfile='/tmp/my_log.log')
        self.log.info("Doing something...")
        self.log.err("Something went wrong...")
        self.log.warn("You shouldn't do this...")
        self.log.debug("Adding numbers...")
        self.log.critical("Save your work immediately...")

Easily specify rotating logs. See __init__() for all option.

NOTE1: 
      since this service is a singleton, the __init__() method
      won't run when another copy of LoggingService is delivered.
      This means:
      
          log1 = LoggingService(logging_level=logging.DEBUG)
        
        log1's logging level is DEBUG. Now:
        
          log2 = LoggingService(logging_level=logging.INFO)
          
        log1's and log2's logging level continues to be DEBUG.
        Until
        
          log2.logging_level = logging.INFO
          
        at which point both log1 and lo2 are at INFO level.

Note2: The logging level default is INFO, i.e. the first LoggingService()
       call will return an instance at logging level INFO, not level
       NOTSET, like the builtin logging facility. This was an oversight
       that is not correctible without breaking backward compatibility.

'''
import logging
from logging.handlers import RotatingFileHandler
import os
import sys


# ----------------------------- Metaclass ---------------------
class MetaLoggingSingleton(type):
    
    def __init__(cls, name, bases, dic):
        super(MetaLoggingSingleton, cls).__init__(name, bases, dic)
        cls.instance = None
    
    def __call__(cls, *args, **kwargs):

        try:
            force = kwargs['force']
            if type(force) != bool:
                raise TypeError(f"Force keyword value must be True or False, not '{force}'")
            # Remove 'force' from kwargs, else the force
            # kwarg is passed to the __init__() method, 
            # which does not expect it:
            del(kwargs['force'])
        except KeyError:
            force = False
            
        if cls.instance is not None and not force:
            return cls.instance
        cls.instance = super(MetaLoggingSingleton, cls).__call__(*args, **kwargs)
        return cls.instance

# ----------------------------- LoggingService Class ---------------------

class LoggingService(metaclass=MetaLoggingSingleton):
    '''
    A singleton logger. Use that single instance
    for multiple modules to log to one place. Methods
    are debug(), warn(), info(), and err(). Can
    log to display or to file.
    
    Easiest use is to create an instance of this class
    (which will always return the same instance for everyone).
    Assign it to a class variable called "log". Then for logging,
    use:
    
         self.log.err()
         self.log.info()
            etc.
     
    '''
        
    #-------------------------
    # __repr__ 
    #--------------
    
    def __repr__(self):
        return f'<LoggingService {hex(id(self))}>'

    #-------------------------
    # Constructor 
    #--------------


    def __init__(self, 
                 logging_level=logging.INFO, 
                 logfile=None,
                 tee_to_console=True,
                 msg_identifier=None,
                 rotating_logs=True,
                 log_size=1000000,
                 max_num_logs=500,
                 logger_name=None):

        '''
        Create a shared logging service.
        Options are logging to screen, or to a file.
        Within file logging choices are whether to log
        to an ever increasing file, or to use the Python
        RotatingFileHandler facility.
        
        @param logging_level: INFO, WARN, ERR, etc as per 
            standard logging module
        @type logging_level: int
        @param logfile: if provided, file path for the log file(s)
        @type logfile: str,
        @param tee_to_console: used only if logfile is provided. If
            True, then also send logs to console
        @type tee_to_console: bool
        @param msg_identifier: if provided this string will
            be shown at the start of each log message. If None,
            the Python module in argv[0] will be shown
        @type msg_identifier: {None|str}
        @param rotating_logs: whether or not to rotate logs. 
        @type rotating_logs: bool
        @param log_size: max size of each log file, if rotating 
        @type log_size: int
        @param max_num_logs: max number of log files before 
            rotating.
        @type max_num_logs: int
        @param logger_name: name by which this logger will be known.
        @type logger_name: str
        '''

        self.name = logger_name
        self._logging_level = logging_level
        self._log_file = logfile
        self.setup_logging(self._logging_level, 
                           self._log_file,
                           tee_to_console=tee_to_console,
                           msg_identifier=msg_identifier,
                           rotating_logs=rotating_logs,
                           log_size=log_size,
                           max_num_logs=max_num_logs,
                           logger_name=logger_name)
        
        
    #-------------------------
    # loggingLevel
    #--------------
    
    @property
    def logging_level(self):
        '''
        Return logging level as dict with 
        level number and name:
        '''
        lvl = self._logging_level
        if lvl == logging.DEBUG:
            return {'number' : logging.DEBUG, 'name': 'DEBUG'}
        if lvl == logging.INFO:
            return {'number' : logging.INFO, 'name': 'INFO'}
        if lvl == logging.WARN:
            return {'number' : logging.WARN, 'name': 'WARN'}
        if lvl == logging.ERROR:
            return {'number' : logging.ERROR, 'name': 'ERROR'}
        if lvl == logging.CRITICAL:
            return {'number' : logging.CRITICAL, 'name': 'CRITICAL'}
        
    @logging_level.setter
    def logging_level(self, new_level):
        self._logging_level = new_level
        LoggingService.logger.setLevel(new_level)

        # Found that need to set logging level
        # for each handler separately:
        
        for one_handler in self.handlers:
            one_handler.setLevel(new_level)
            
    def setLevel(self, new_level):
        '''
        Compatibility with standard logger
        
        :param new_level: new level
        :type new_level: int
        '''
        self.logging_level = new_level

    #-------------------------
    # logFile 
    #--------------
        
    @property
    def log_file(self):
        return self._log_file
    
    @log_file.setter
    def log_file(self, new_file):
        
        self._log_file = new_file
        # Remove the old logging handler.
        # Doesn't throw error if it's not there:

        for one_handler in LoggingService.logging_handlers:
            LoggingService.logger.removeHandler(one_handler)
        # Make a whole new logger with the
        # proper log file dest. This LoggingService 
        # instance will still be the same: 
        LoggingService.setup_logging(self.logging_level, 
                                     new_file, 
                                     LoggingService.tee_to_console,
                                     LoggingService.msg_identifier, 
                                     LoggingService.rotating_logs, 
                                     LoggingService.log_size, 
                                     LoggingService.max_num_logs,
                                     logger_name=self.logger.name
                                     )

    #-------------------------
    # handlers 
    #--------------
    
    @property
    def handlers(self):
        return self.logger.handlers

    #-------------------------
    # setup_logging 
    #--------------
    
    @classmethod
    def setup_logging(cls, 
                      loggingLevel=logging.INFO, 
                      logFile=None,
                      tee_to_console=True,
                      msg_identifier=None,
                      rotating_logs=True,
                      log_size=1000000,
                      max_num_logs=500,
                      logger_name=None
                      ):
        '''
        Set up the standard Python logger.
        If msg_identifier is provided, it is shown
        at the very start of each logging message.
        If None, the file name of the calling module
        is used without the .py extension.

        @param loggingLevel: initial logging level
        @type loggingLevel: {logging.INFO|WARN|ERROR|DEBUG}
        @param logFile: optional file path where to send log entries
        @type logFile: str
        '''
        
        # Save parms in case someone changes the
        # logfile on this logger later:

        cls.msg_identifier = msg_identifier
        cls.rotating_logs  = rotating_logs
        cls.log_size       = log_size
        cls.tee_to_console = tee_to_console
        cls.max_num_logs   = max_num_logs
        
        # Make the name of the logger be the name
        # of this file, without the .py extension:
        if logger_name is None:
            (logger_name, _ext) = os.path.splitext(os.path.basename(__file__))
        the_logger = logging.getLogger(logger_name)
        if the_logger.hasHandlers():
            while len(the_logger.handlers) > 0:
                the_logger.removeHandler(the_logger.handlers[-1])
        the_logger.setLevel(loggingLevel)
        LoggingService.logger = the_logger 

        # Add handlers as needed:
        handlers = []
        # Create file handler if requested:
        if logFile is not None:
            if rotating_logs:
                # New log file every 10Mb, at most 500 times:
                handler = RotatingFileHandler(logFile,
                                              maxBytes=log_size,
                                              backupCount=max_num_logs
                                              )
            else:
                handler = logging.FileHandler(logFile)
                
            handlers.append(handler)
            # Also log to console?
            if tee_to_console:
                handlers.append(logging.StreamHandler(sys.stdout))
            # print('Logging of control flow will go to %s' % logFile)
        else:
            # Create console handler:
            handler = logging.StreamHandler()
            handlers.append(handler)

        # Create formatter
        #formatter = logging.Formatter("%(name)s: %(asctime)s;%(levelname)s: %(message)s")
        if msg_identifier is None:
            cls.msg_identifier = os.path.basename(sys.argv[0])

        formatter = logging.Formatter(f"{cls.msg_identifier}({os.getpid()}): %(asctime)s;%(levelname)s: %(message)s")

        # Avoid double entries from the default logger:
        LoggingService.logger.propagate = False        

        # Set the handler(s) logging level,
        # their formatter, and add them to 
        # the logger
        for one_handler in handlers:
            one_handler.setLevel(loggingLevel)
            one_handler.setFormatter(formatter)
            LoggingService.logger.addHandler(one_handler)
        
            
        # Remember handler obj(s) so we can remove them if 
        # a new logfile is requested:
        cls.logging_handlers = handlers
        LoggingService.logger.setLevel(loggingLevel)

    #-------------------------
    # log_debug/warn/info/err/critical 
    #--------------

    def debug(self, msg):
        LoggingService.logger.debug(msg)

    def warn(self, msg):
        LoggingService.logger.warning(msg)

    def info(self, msg):
        LoggingService.logger.info(msg)

    def err(self, msg):
        LoggingService.logger.error(msg)
        
    def critical(self, msg):
        LoggingService.logger.critical(msg)

# ------------------------- Main ---------------

# For testing only; this module is intended for import.
if __name__ == '__main__':
    pass 
    
#    l = LoggingService()
#    print(l)
#    lsame = LoggingService()
#    print(lsame)
#     l1 = LoggingService(log_file='/tmp/trash.log')
#     print(l1)
#     l1same = LoggingService(log_file='/tmp/trash.log')
#     print(l1same)
#     l2 = LoggingService()
#     print(l2)

#     l = LoggingService(log_file='/tmp/trash.log',
#                        rotating_logs=True,
#                        log_size=10,
#                        max_num_logs=4
#                        )
#     l.info('123456789')
#     
    
