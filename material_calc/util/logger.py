import logging
import os
import time

from logging.handlers import RotatingFileHandler

APP_NAME = "APP"


def getLogger(name):
  # 日志地址
  log_file_folder = "logs"
  # 文件名，以日期作为文件名
  log_file_name = 'app.' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
  # log_file_error_name = 'app.error.' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'

  log_file_str = log_file_folder + os.sep + log_file_name
  # log_file_error_str = log_file_folder + os.sep + log_file_error_name

  if not os.path.exists(log_file_folder):
    os.makedirs(log_file_folder)

  format = logging.Formatter(fmt='%(asctime)s.%(msecs)03d  %(levelname)s %(filename)s:%(lineno)d  %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

  # 默认日志等级的设置
  logger = logging.getLogger(name)
  logger.setLevel(level=logging.INFO)

  # 控制台日志
  std_handler = logging.StreamHandler()
  std_handler.setLevel(logging.INFO)
  std_handler.setFormatter(format)
  logger.addHandler(std_handler)

  # 运行日志
  f_handler = RotatingFileHandler(log_file_str, maxBytes=1024 * 1024, backupCount=10, encoding="UTF-8")
  f_handler.setLevel(logging.INFO)
  f_handler.setFormatter(format)
  logger.addHandler(f_handler)

  # 错误日志
  # e_handler = RotatingFileHandler(log_file_error_str, maxBytes=1024 * 1024, backupCount=10, encoding="UTF-8")
  # e_handler.setLevel(logging.ERROR)
  # e_handler.setFormatter(format)
  # logger.addHandler(e_handler)
  return logger


logs = getLogger(APP_NAME)
