from doit.action import CmdAction

def task_pytest():
  """run pytest"""
  return {
    'actions': ["""PYTHONPATH=`pwd`/src pytest --color=yes"""], 
    'verbosity': 2
  }

def task_pytestv():
  """run pytest"""
  return {
    'actions': ["""PYTHONPATH=`pwd`/src pytest -v --color=yes"""],
    'verbosity': 2
  }

def task_cov():
  """check test coverage"""
  return {
    'actions': ["""PYTHONPATH=`pwd`/src pytest --color=yes --cov=src"""], 
    'verbosity': 2
  }

def task_fixit():
  """run fixit in lint mode"""
  return {
    'actions': ['fixit lint src']
  }

def task_fix():
  """run fixit in fix mode"""
  return {
    'actions': ['fixit fix src']
  }
