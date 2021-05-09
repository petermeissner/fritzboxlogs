import datetime

def timestamp(format: str = "%Y-%m-%d %H:%M:%S") -> str:
  """
  Function generating timestamp string. 

  Args:
      format (str, optional): The format to use for timestamp. Defaults to "%Y-%m-%d %H:%M:%S".

  Returns:
      str: formatted timestamp
  """

  # generate current time with given format
  ts = datetime.datetime.now().strftime(format)

  # return
  return ts
