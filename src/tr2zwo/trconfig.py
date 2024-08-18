import sys
import keyring
from getpass import getpass


class TRConfig:
  verbose: bool = False
  username: str = ''
  password: str = ''
  directory: str = ''

  def __init__(self):
    self.load()

  def save(self):
    keyring.set_password('tr2zwift', 'username', self.username)
    keyring.set_password('tr2zwift', 'password', self.password)
    keyring.set_password('tr2zwift', 'directory', self.directory)

  def load(self):
    self.username = keyring.get_password('tr2zwift', 'username')
    self.password = keyring.get_password('tr2zwift', 'password')
    self.directory = keyring.get_password('tr2zwift', 'directory')

  def setup(self, username='', password='', directory=''):

    if username:
      self.username = username
    else:
      self.username = input('TrainerRoad username: ')
      keyring.set_password('tr2zwift', 'username', self.username)

    if password:
      self.password = password
    else:
      self.password = getpass('TrainerRoad password: ')
      keyring.set_password('tr2zwift', 'password', self.password)

    if directory:
      self.directory = directory
    else:
      self.directory = input('Output directory for .zwo files: ')
      keyring.set_password('tr2zwift', 'directory', self.directory)

  def dump(self):
    print(f'username: {self.username}')
    print(f'password: {self.password}')
    print(f'directory: {self.directory}')


# ==============================================================================
def main():
  c = TRConfig()
  c.dump()


# ===============================================================================
if __name__ == '__main__':
  sys.exit(main())
