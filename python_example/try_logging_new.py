        
import logging
import time
import sys
import os


class Logger:
    # 日志级别关系映射
    level_relations = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }

    def __init__(self, level="info", logger_name="Unknown.log"):
        self.log_level = level
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        # create log folder and add it as a property of self.logger
        self.logger.log_path = self.set_path()
        # set addFileHandler as a property of self.logger: add_log
        self.logger.add_log = self.addFileHandler
        # set removeFileHandler as a property of self.logger: add_log
        self.logger.remove_log = self.removeFileHandler
        self.formater = logging.Formatter(
            '[%(asctime)s][%(filename)s line:%(lineno)d][%(levelname)s]: %(message)s')

        # set log to file
        self.logname = os.path.join(self.logger.log_path, logger_name)
        if os.path.isfile(self.logname):
            os.remove(self.logname)
        # 设置日志输出到文件（指定间隔时间自动生成文件的处理器  --按日生成）
        # filename：日志文件名，interval：时间间隔，when：间隔的时间单位， backupCount：备份文件个数，若超过这个数就会自动删除
        # self.filelogger  = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backupCount, encoding="utf-8")
        self.filelogger = logging.FileHandler(
            self.logname, mode='a', encoding="UTF-8")
        self.filelogger.setLevel(self.level_relations.get(self.log_level))
        self.filelogger.setFormatter(self.formater)
        # set log to console
        self.console = logging.StreamHandler()
        self.console.setLevel(self.level_relations.get(self.log_level))
        self.console.setFormatter(self.formater)
        # add file handler
        self.logger.addHandler(self.filelogger)
        # add console handler
        self.logger.addHandler(self.console)

    def addFileHandler(self, file_name=None):
        # add new file handler
        new_log_file = os.path.join(self.logger.log_path, file_name)
        new_log_path = os.path.dirname(new_log_file)
        if not os.path.exists(new_log_path):
            try:
                os.makedirs(new_log_path)
            except Exception as err:
                print(f'[ERROR] Failed init case logger when create log file: {new_log_path}, error:{err} ')
                sys.exit(1)
        new_filelogger = logging.FileHandler(
            new_log_file, mode='a', encoding="UTF-8")
        # TODO: we can set a diffierent log_level &&formater for this new FileHandle here
        new_filelogger.setLevel(self.level_relations.get(self.log_level))
        new_filelogger.setFormatter(self.formater)
        self.logger.addHandler(new_filelogger)

    def removeFileHandler(self):
        # will remove handler with stream.fileno > 3, this means only keep self.filelogger and self.console
        for handler in self.logger.handlers:
            if handler.stream.fileno() > 3:
                self.logger.removeHandler(handler)

    def set_path(self):
        base_path = os.path.dirname(
            os.path.dirname(os.path.realpath(__file__)))
        now = time.strftime("%Y_%m_%d_%H_%M_%S")
        log_path = os.path.join(base_path, "logs", now)
        if not os.path.exists(log_path):
            try:
                os.makedirs(log_path)
            except Exception as err:
                print(f'[ERROR] Failed init logger when create log file: {log_path}, error:{err}')
                sys.exit(1)
        return log_path

    if not __name__ == '__main__':
        logger = Logger(level="debug", logger_name="MY_TEST.log").logger
