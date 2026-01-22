import logging

from coverage_ai.settings.config_loader import get_settings


class CustomLogger:

    @classmethod
    def get_logger(
        cls,
        name,
        generate_log_files=True,
        file_level=logging.INFO,
        console_level=logging.INFO,
    ):
        """
        Return a logger object with specified name.

        Parameters:
            name (str): The name of the logger.
            generate_log_files (bool): Whether to generate log files.
            file_level (int): The log level to use.
            console_level (int): The log level to use.

        Returns:
            logging.Logger: The logger object.

        Note:
            This method sets up the logger to handle all messages of DEBUG level and above.
            It adds a file handler to write log messages to a file specified by 'log_file_path' and a stream handler
            to output log messages to the console. The log file is overwritten on each run.

        Example:
            logger = CustomLogger.get_logger('my_logger')
            logger.debug('This is a debug message')
            logger.info('This is an info message')
            logger.warning('This is a warning message')
            logger.error('This is an error message')
            logger.critical('This is a critical message')
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Ensure stream handler is present
        if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(console_level)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

        # Sync file handler state with generate_log_files flag
        file_handlers = [
            h for h in logger.handlers if isinstance(h, logging.FileHandler)
        ]
        if generate_log_files and not file_handlers:
            log_file_path = get_settings().get("default").get("log_file_path", "run.log")
            file_handler = logging.FileHandler(log_file_path, mode="w")
            file_handler.setLevel(file_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        elif not generate_log_files:
            for handler in file_handlers:
                logger.removeHandler(handler)
                handler.close()

            # Prevent log messages from being propagated to the root logger
            logger.propagate = False

        return logger
