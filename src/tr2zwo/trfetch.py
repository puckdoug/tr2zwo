import re
import httpx
from typing import List, Dict, Optional
from argparse import ArgumentParser
import sys
import msgspec
from bs4 import BeautifulSoup
from tr2zwo import TRConfig

# ===============================================================================
class TRFetch(msgspec.Struct):
  _client: Optional[httpx.Client] = None
  _login: Optional[httpx.Response] = None
  raw: str = ''
  verbose: bool = False
  workouts: List[Dict] = []

  # -------------------------------------------------------------------------------
  def login(self, fh=sys.stdout):
    c = TRConfig()
    url = 'https://www.trainerroad.com/app/login'
    self._client = httpx.Client(follow_redirects=True)
    if self.verbose:
      print('Logging in to TrainerRoad', file=fh)

    login_page = self._client.get(url) # just fetch the page
    soup = BeautifulSoup(login_page.text, 'lxml')

    # set up the form data
    data = {}
    data['Username'] = c.username
    data['Password'] = c.password
    for hidden in soup.form.find_all('input', type='hidden'):
      data[hidden['name']] = hidden['value']

    # post the form
    self._login = self._client.post(url, data=data, cookies=self._client.cookies)

  # -------------------------------------------------------------------------------
  def fixup_endpoint(self, endpoint):
    id = re.search(r'workouts/(\d+)-?', endpoint).group(1)
    return f'https://www.trainerroad.com/app/api/workoutdetails/{id}'

  # -------------------------------------------------------------------------------
  def fetch_workout(self, endpoint, fh=sys.stdout):
    if self._client is None:
      self.login(fh=fh)

    detail = self.fixup_endpoint(endpoint)
    if self.verbose:
      print(f'fetching {detail}', file=fh)

    workout = self._client.get(detail)

    self.raw = workout.text
    trr = workout.json()

    return trr


# ------------------------------------------------------------------------------
def main():
  p = ArgumentParser(
    description='Convert a TrainerRoad workout to a Zwift .zwo file'
  )
  p.add_argument(
    '--verbose',
    '-v',
    action='store_const',
    const=True,
    help='provide feedback while running',
  )
  p.add_argument(
    '--raw',
    '-r',
    action='store_const',
    const=True,
    help='output raw retult of the query',
  )
  p.add_argument(
    '--setup',
    '-s',
    action='store_const',
    const=True,
    help='initial setup, can be run again to update settings',
  )
  p.add_argument('--username', '-u', help='Your TrainerRoad username')
  p.add_argument('--password', '-p', help='Your TrainerRoad password')
  p.add_argument(
    'url', nargs='+', help='The URL(s) of the trainerroad workout(s) to fetch'
  )
  args = p.parse_args()

  f = TRFetch()

  if args.setup:
    print('Not implemented yet')
    exit(0)

  if args.verbose:
    f.verbose = True

  workouts = []

  for u in args.url:
    w = f.fetch_workout(u)
    workouts.append(w)
    if args.verbose:
      print(f"Added workout '{w['Workout']['Details']['WorkoutName']}'")
    if args.raw:
      print(f.raw)


# ===============================================================================
if __name__ == '__main__':
  main()
