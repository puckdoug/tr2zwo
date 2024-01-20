#!/usr/local/bin/python3
"""Command-line wrapper"""
import sys
from argparse import ArgumentParser
from trfetch import TRFetch
from trworkout import Workout

#==============================================================================
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

  if args.verbose:
    f.verbose = True

  for u in args.url:
    data = f.fetch_workout(u)
    w = Workout.create(raw=data)
    w.dump_xml()

#===============================================================================
if __name__ == '__main__':
    sys.exit(main())
