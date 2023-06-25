import os
from shutil import rmtree


def del_file(file_name: str):
  """
  下载完成后删除文件
  :param file_name:
  :return:
  """
  os.remove(file_name)


def del_path(path: str):
  """
  删除目录
  :param path:
  :return:
  """
  rmtree(path)
