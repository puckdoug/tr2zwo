"""Command-line wrapper"""
import sys
from argparse import ArgumentParser
from tr2zwo import TRFetch, Workout, TRConfig
from typing import Optional


# ==============================================================================
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
  sub = p.add_subparsers(dest='cmd')
  setup = sub.add_parser(
    'setup', help='initial setup, can be run again to update settings'
  )
  setup.add_argument('--username', '-u', help='Your TrainerRoad username')
  setup.add_argument('--password', '-p', help='Your TrainerRoad password')
  setup.add_argument(
    '--directory', '-d', help='Output directory for .zwo file  s'
  )
  fetch = sub.add_parser('fetch', help='fetch one or more workouts')
  fetch.add_argument(
    '--print',
    '-p',
    action='store_const',
    const=True,
    help='Print the zwo to stdout, does not write file',
  )
  fetch.add_argument(
    'url', nargs='+', help='The URL(s) of the trainerroad workout(s) to fetch'
  )
  fetch.add_argument(
    '--raw',
    '-r',
    action='store_const',
    const=True,
    help='output raw retult of the query',
  )
  args = p.parse_args()

  c = TRConfig()
  if args.verbose:
    c.verbose = True

  match args.cmd:
    case 'setup':
      user: Optional[str]
      pasw: Optional[str]
      dire: Optional[str]
      try:
        user = args.username
        if user is None:
          user = ''
      except AttributeError:
        user = ''
      try:
        pasw = args.password
        if pasw is None:
          pasw = ''
      except AttributeError:
        pasw = ''
      try:
        dire = args.directory
        if dire is None:
          dire = ''
      except AttributeError:
        dire = ''
      c.setup(username=user, password=pasw, directory=dire)
    case 'fetch':
      f = TRFetch(verbose=c.verbose)
      for u in args.url:
        data = f.fetch_workout(u)
        w = Workout.create(raw=data, url=u, verbose=c.verbose)
      if args.print:
        w.print()
      elif args.raw:
        w.print_raw()
      else:
        w.write(directory=c.directory)
    case _:
      p.print_help()


# ===============================================================================
if __name__ == '__main__':
  sys.exit(main())
