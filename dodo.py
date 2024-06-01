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
    'actions': ['fixit lint src'],
    'verbosity': 2
  }

def task_mypy():
  """run mypy"""
  return {
    'actions': ['mypy src'],
    'verbosity': 2
  }

def task_fix():
  """run fixit in fix mode"""
  return {
    'actions': ['fixit fix src']
  }

def task_flake8():
  """run flake8 on src and test"""
  return {
    'actions': ['flake8 src test']
  }

def task_build():
  """build package"""
  return {
    'actions': [ 'pyproject-build' ],
    'verbosity': 2
  }

def task_format():
  """run ruff format"""
  return {
    'actions': [ 'ruff format src' ],
  }

def task_cleanup():
  """clean up build artifacts"""
  return {
    'actions': [ 'rm -rf build tr2zwift.spec dist src/tr2zwo.egg-info src/tr2zwift src/tr2zwift-gui' ]
  }

def task_watch():
  """run pytest on continuous loop whenever a file is updated"""
  return {
    'actions': ["""watchmedo shell-command --patterns="*.py" --recursive --command='PYTHONPATH=`pwd`/src pytest --color=yes' ."""],
    'verbosity': 2
  }
