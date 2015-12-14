#!/usr/bin/python
def half(x):
  """Halves x.  For example:
  >>> half(6.8)
  3.3
  >>>
  """
  return x/2


if __name__ == "__main__":
  import doctest
  doctest.testmod(verbose=True)
