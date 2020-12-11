# Singleton Logging Service

Logging service that is guaranteed to be a singleton. Based on Python logging,
but every instantiation of LoggingService from any of an application's modules
returns the same logger instance. Uses RotatingFileHandler by default.

Code example:

        from logging_service import LoggingService

        self.log = LoggingService()

        self.log.info("Constructing output file names...")
        self.log.err("Failed to construct output file names...")
        self.log.warn("Output file names are unusual...")
        self.log.debug("Constructing output file names foo.bar, fum.txt...")

If another module imports and instantiates LoggingService() as per above,
the same logger instance will be used.

This API is more primitive than the hierarchical native logging module,
but hopefully simple to use. One can log to a file, or to the console.
One formatter is built in for info/debug/warn/err. Example:

`my_module.py(290375): 2020-09-03 14:58:33,017;INFO: Start Epoch [1/50]`

When first creating a LoggingService instance, the following options
are available in the constructor; all are optional:

    logging_level=logging.INFO, 
    logfile=None,
    msg_identifier=None,
    rotating_logs=True,
    log_size=1000000,
    max_num_logs=500,
    logger_name=None

After creation a logger instance may only be modified like this:

    - my_logger.logging_level = logging.NEW_LEVEL
    - my_logger.log_file      = '/tmp/new_logfile'

where logging levels are the usual `logging.INFO,` `logging.WARN`, etc.


