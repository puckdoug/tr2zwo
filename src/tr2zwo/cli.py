#!/usr/local/bin/python3
"""Command-line wrapper"""
import sys
from argparse import ArgumentParser
from getpass import getpass
from tr2zwo import TRFetch, Workout, TRConfig

#==============================================================================
def main():

  p = ArgumentParser(
    description="Convert a TrainerRoad workout to a Zwift .zwo file")
  p.add_argument('--verbose', '-v', action='store_const',
    const=True, help="provide feedback while running")
  sub =  p.add_subparsers(dest='cmd')
  setup = sub.add_parser('setup', help="initial setup, can be run again to update settings")
  setup.add_argument('--username', '-u', help="Your TrainerRoad username")
  setup.add_argument('--password', '-p', help="Your TrainerRoad password")
  setup.add_argument('--directory', '-d', help="Output directory for .zwo file  s")
  fetch = sub.add_parser('fetch', help="fetch a workout")
  fetch.add_argument('--print', '-p', action='store_const', const=True,
    help="Print the zwo to stdout, does not write file")
  fetch.add_argument('url', nargs='+',
    help="The URL(s) of the trainerroad workout(s) to fetch")
  # fetch.add_argument('--raw', '-r', action='store_const',
  #   const=True, help="output raw retult of the query")
  args = p.parse_args()

  if args.verbose:
    f.verbose = True

  c = TRConfig()

  match args.cmd:
    case 'setup':
      try:
        u = args.username
      except AttributeError:
        u = None
      try:
        p = args.password
      except AttributeError:
        p = None
      try:
        d = args.directory
      except AttributeError:
        d = None
      c.setup( username=u, password=p, directory=d )
    case 'fetch':
      f = TRFetch()
      for u in args.url:
        data = f.fetch_workout(u)
        w = Workout.create(raw=data)
      if args.print:
        w.print()
      else:
        w.write(directory=c.directory)
    case _:
      p.print_help()


#===============================================================================
if __name__ == '__main__':
    sys.exit(main())
