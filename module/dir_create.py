import os


def dir_create(path: str, ignore_exists=False) -> None:
  """
  Simple wrapper around `os.mkdir()` with some helpful defaults.

  Args:
      path (str): [description]
      ignore_exists ([type]): [description]
  """
  path = os.path.expanduser(path)
  if ignore_exists:
    
    try:
      os.mkdir(path)
    except FileExistsError:
      pass

  else:
    os.mkdir(path)
