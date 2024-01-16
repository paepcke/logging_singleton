# Singleton Logging Service

Logging service that is guaranteed to be a singleton. Based on Python logging, but every instantiation of LoggingService from any of an application's modules returns the same logger instance.

###Examples:

        from logging_service import LoggingService

        self.log = LoggingService()

        self.log.info("Constructing output file names...")
        self.log.err("Failed to construct output file names...")
        self.log.warn("Output file names are unusual...")
        self.log.debug("Constructing output file names foo.bar, fum.txt...")

This API is more primitive than the hierarchical native logging module, but hopefully simple to use. One can:

        - Log to a file,
        - The console, or
        - Both
        
A single formatter is built in for info/debug/warn/err. Example:

`my_module.py(290375): 2020-09-03 14:58:33,017;INFO: Start Epoch [1/50]`

When first creating a LoggingService instance, the following options
are available in the constructor; all are optional:

    logging_level=logging.INFO    # the Python logging package's constants
    logfile=None,                 # destination file; None implies console only
    tee_to_console=True,          # if logfile is specified, also log to console
    msg_identifier=None,          # shown at start of each msg; default is module name
    rotating_logs=True,           # if logging to file, rotate log if size exceeded
    log_size=1000000,             # max log size for rotation
    max_num_logs=500,             # max number of full logs to retain
    logger_name=None              # name for the logger instance

After creation a logger instance may only be modified like this:

    - my_logger.logging_level = logging.NEW_LEVEL
    - my_logger.log_file      = '/tmp/new_logfile'

where logging levels are the usual `logging.INFO,` `logging.WARN`, etc.


