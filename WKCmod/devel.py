#! /usr/env/python
# encoding: UTF-8 - 

def info(object, spacing=10, collapse=1):
  """Print methods and doc strings.
  Takes module, class, list, dictionary, or string."""
  
  methodList = [method for method in dir(object)]
  
  processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
  
  print "\n".join(["%s %s" %
  (method.ljust(spacing),
  processFunc(str(getattr(getattr(object, method),'__doc__',None))))
  for method in methodList])

