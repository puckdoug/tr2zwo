#!/usr/local/bin/python3

import re
import httpx
import keyring
from typing import List, Dict
from argparse import ArgumentParser
import msgspec

#===============================================================================
class TRFetch(msgspec.Struct):
  _client: httpx.Client = None
  _login: httpx.Response = None
  verbose: bool = False
  workouts: List[Dict] = []

#-------------------------------------------------------------------------------
  def login(self):
    url = "https://www.trainerroad.com/app/login"
    self._client = httpx.Client(follow_redirects=True)
    if self.verbose:
      print("Logging in to TrainerRoad")
    username = keyring.get_password('trainerroad', 'username')
    password = keyring.get_password('trainerroad', 'password')
    data = { "Username": username, "Password": password }
    self._login = self._client.post(url, data=data )

#-------------------------------------------------------------------------------
  def fixup_endpoint(self, endpoint):
    id = re.search(r"workouts/(\d+)-", endpoint).group(1)
    return f"https://www.trainerroad.com/app/api/workoutdetails/{id}"

#-------------------------------------------------------------------------------
  def fetch_workout(self, endpoint):
    if self._client is None:
      self.login()

    detail = self.fixup_endpoint(endpoint)
    if self.verbose:
      print(f"fetching {detail}")
    workout = self._client.get(detail)

    trr = workout.json()

    return trr

#------------------------------------------------------------------------------
def main():

  p = ArgumentParser(
    description="Convert a TrainerRoad workout to a Zwift .zwo file")
  p.add_argument('--verbose', '-v', action='store_const',
    const=True, help="provide feedback while running")
  p.add_argument('--setup', '-s', action='store_const',
    const=True, help="initial setup, can be run again to update settings")
  p.add_argument('--username', '-u', help="Your TrainerRoad username")
  p.add_argument('--password', '-p', help="Your TrainerRoad password")
  p.add_argument('url', nargs='+',
    help="The URL(s) of the trainerroad workout(s) to fetch")
  args = p.parse_args()

  f = TRFetch()

  if args.setup:
    print("Not implemented yet")
    exit(0)

  if args.verbose:
    f.verbose = True

  workouts = []

  for u in args.url:
    w = f.fetch_workout(u)
    workouts.append(w)
    if args.verbose:
      print(f"Added workout '{w['Workout']['Details']['WorkoutName']}'")

#===============================================================================
if __name__ == '__main__':
  main()
