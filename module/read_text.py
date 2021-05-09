import os
from typing import List, Union


def read_text(
  path:    str, 
  as_list: bool = False
) -> Union[str, List[str]]:
  # read in text
  with open(os.path.expanduser(path)) as f:
    res = f.readlines()

  # string or list?
  if as_list == True:
    pass
  else:
    res = ''.join(res)

  # return 
  return res
