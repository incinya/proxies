import logging  # 引入logging模块
import os
import time


def logger():
    logging.basicConfig(level=logging.NOTSET)  # 设置日志级别
    # 第一步，创建一个logger
    _logger = logging.getLogger()
    _logger.setLevel(logging.NOTSET)  # Log等级总开关

    # 第二步，创建一个handler，用于写入日志文件
    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))

    log_path = os.getcwd()
    logfile = os.path.join(log_path, rq + '.log')
    fh = logging.FileHandler(logfile, mode='a')
    fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
    # 第三步，定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    # 第四步，将logger添加到handler里面
    _logger.addHandler(fh)

    logging.debug('hello world')
    return logging
