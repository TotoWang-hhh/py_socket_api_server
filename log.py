""" 日志功能 """
import logging
import os
import time

ColorLevel = {
    "[CRITICAL]": "[\033[35mCRITICAL\033[0m]",  # purple
    "[ERROR]": "[\033[31mERROR\033[0m]",  # red
    "[WARNING]": "[\033[33mWARNING\033[0m]",  # yellow
    "[INFO]": "[\033[36mINFO\033[0m]",  # blue
    "[DEBUG]": "[\033[32mDEBUG\033[0m]",  # green
}


class ColorStreamHandler(logging.StreamHandler):
    # 继承重写: 给日志上色！
    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            stream = self.stream
            for key, value in ColorLevel.items():  # This for loop relized colorlevel.
                msg = msg.replace(key, value)
            # issue 35046: merged two stream.writes into one.
            stream.write(msg + self.terminator)
            self.flush()
        except RecursionError:  # See issue 36272
            raise
        except Exception:
            self.handleError(record)


def check_log() -> None:
    """ 检查日志大小 """
    global logfile
    try:
        if flag := os.path.getsize(logfile) >= (1 << 20):
            _time = time.strftime("%Y%m%d%H%M%S", time.localtime())
            logfile = "./logs/%s.log" % _time
        logger.info('日志大小检查, 结果: %s' % flag)
        from timer import Countdown
        Countdown(86400, check_log)
    except Exception as error:
        logger.error('检查日志大小时出错, %s' % error)


logfile = "./logs/%s.log" % time.strftime("%Y%m%d%H%M%S", time.localtime())


datefmt = "%Y-%m-%d %H:%M:%S"
handler_console = ColorStreamHandler()
handler_console.setLevel("WARN")
fmt_console = "\r\033[36m%(asctime)s.%(msecs)03d\033[0m [%(levelname)s] (%(filename)s) %(funcName)s: %(message)s"
handler_console.setFormatter(logging.Formatter(fmt_console, datefmt))
handler_file = logging.FileHandler(logfile)
handler_file.setLevel("DEBUG")
fmt_file = "%(asctime)s.%(msecs)03d [%(levelname)s] (%(filename)s) %(funcName)s: %(message)s"
handler_file.setFormatter(logging.Formatter(fmt_file, datefmt))

logger = logging.getLogger()
logger.setLevel("DEBUG")
logger.addHandler(handler_console)
logger.addHandler(handler_file)


if __name__ == "__main__":
    logger.debug('#=== 日志功能测试 ===#')
    logger.debug("program testing")
    logger.info("normal operation")
    logger.warning("Defects in certain functions")
    logger.error("Triggered some program errors")
    logger.critical("Program termination")
    logger.debug('#=== 日志功能测试 ===#')
