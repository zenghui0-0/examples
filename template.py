import os
import sys
import time
import argparse
import logging
from logging import handlers



class Logger(object):
    # 日志级别关系映射
    level_relations = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }

    def __init__(self, filename="log/test.log", level="info", when="D", backupCount=3, fmt="%(asctime)s - %(pathname)s[line:%(lineno)d] - %"
            "(levelname)s: %(message)s"):
        # 设置日志输出格式
        format_str = logging.Formatter(fmt)
        # 设置日志在控制台输出
        streamHandler = logging.StreamHandler()
        # 设置控制台中输出日志格式
        streamHandler.setFormatter(format_str)
        # 设置日志输出到文件（指定间隔时间自动生成文件的处理器  --按日生成）
        # filename：日志文件名，interval：时间间隔，when：间隔的时间单位， backupCount：备份文件个数，若超过这个数就会自动删除
        fileHandler = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backupCount, encoding="utf-8")
        # 设置日志文件中的输出格式
        fileHandler.setFormatter(format_str)
        # 设置日志输出文件
        self.logger = logging.getLogger(filename)
        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))
        # 将输出对象添加到logger中
        self.logger.addHandler(streamHandler)
        self.logger.addHandler(fileHandler)




if __name__ == "__main__":

    #parse argvs
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-r', '--required', required=True,
                        help="required input")
    parser.add_argument('-o', '--optional',
                        help="optional input")
    args = parser.parse_args()
    required = args.required

    #set up log
    PWD = os.getcwd()
    TMP = os.path.join(PWD, "temp")
    if not os.path.isdir(TMP):
        try:
            os.makedirs(TMP)
        except Exception as e:
            assert False, "Error: {} while creating directors:{}".format(e, TMP)
    now = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    LOG = os.path.join(TMP, "run_log_{}.txt".format(now))
    if os.path.isfile(LOG):
        os.remove(LOG)
    log = Logger(filename=LOG, level="debug").logger

    #try log 
    log.info("test info level log")
