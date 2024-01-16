#!/usr/local/bin/python3
import httpx
import ujson
import pprint
from typing import List, Dict
import msgspec
from argparse import ArgumentParser

#------------------------------------------------------------------------------
class WorkoutItem(msgspec.Struct):
  raw: Dict = None
  seconds: int = 0
  ftp: float = 0.0
  member_ftp: float = 0.0

  @classmethod
  def create(cls, **kwargs):
    instance = WorkoutItem()
    if 'raw' in kwargs:
      instance.raw = kwargs['raw']
      instance.seconds = instance.raw['seconds']
      instance.ftp = instance.raw['ftpPercent']
      instance.member_ftp = instance.raw['memberFtpPercent']
    return instance
  
#------------------------------------------------------------------------------
class Interval(msgspec.Struct):
  raw: Dict = None
  start: int = 0
  end: int = 0
  name: str = ""
  power: float = 0.0
  power_max: float = 0.0
  power_max_when: int = 0
  power_min: float = -1.0
  power_min_when: int = 0
  ramp_direction: str = ""
  is_fake: bool = False
  test_interval: bool = False
  wd: List[WorkoutItem] = []
  interval_type: str = ""
  xml: str = ""

#------------------------------------------------------------------------------
  @classmethod
  def create(cls, **kwargs):
    instance = Interval()
    if 'raw' in kwargs:
      instance.raw = kwargs['raw']
      instance.start = instance.raw['Start']
      instance.end = instance.raw['End']
      instance.name = instance.raw['Name']
      instance.is_fake = instance.raw['IsFake']
      instance.test_interval = instance.raw['TestInterval']
      instance.power = instance.raw['StartTargetPowerPercent']
    return instance

#------------------------------------------------------------------------------
  def include(self, workout_item):
    if self.start <= workout_item.seconds / 1000 and self.end > workout_item.seconds / 1000:
      self.wd.append(workout_item)

#------------------------------------------------------------------------------
  def ramp_analysis(self):
    for w in self.wd:
      if self.power_max < w.ftp:
        self.power_max = w.ftp
        self.power_max_when = w.seconds / 1000
      if self.power_min > w.ftp or self.power_min < 0:
        self.power_min = w.ftp
        self.power_min_when = w.seconds / 1000
    if self.power_min_when < self.power_max_when:
      self.ramp_direction = "up"
    else:
       self.ramp_direction = "down"

#------------------------------------------------------------------------------
  def find_type(self):
    if self.wd[0].ftp == self.wd[-1].ftp:
      self.interval_type = "SteadyState"
    else:
      self.interval_type = "Ramp"
      self.ramp_analysis()

#------------------------------------------------------------------------------
  def to_xml(self):
    match self.interval_type:
      case "SteadyState":
        self.xml = f'<SteadyState Duration="{self.end - self.start}" Power="{self.power / 100}"></SteadyState>'
      case "Ramp":
        if self.ramp_direction == "up":
          self.xml = f'<Ramp Duration="{self.end - self.start}"' + \
                     f' PowerLow="{self.power_min / 100}"' + \
                     f' PowerHigh="{float(round(self.power_max) / 100)}"></Ramp>'
        else:
          self.xml = f'<Ramp Duration="{self.end - self.start}"' + \
                     f' PowerLow="{self.power_max / 100}"' + \
                     f' PowerHigh="{float(round(self.power_min) / 100)}"></Ramp>'
      case _:
        self.xml = f'<unknown></unknown>'
    
#------------------------------------------------------------------------------
class Workout(msgspec.Struct):
  raw: Dict = None
  author: str = 'TrainerRoad'
  name: str = None
  description: str = None
  category: str = 'TrainerRoad'
  sport: str = 'bike'
  intervals: List[Interval] = []
  workout_items: List[WorkoutItem] = []

#------------------------------------------------------------------------------
  @classmethod
  def create(cls, **kwargs):
    instance = Workout()
    if 'raw' in kwargs:
      instance.raw = kwargs['raw']
      instance.name = instance.raw['Workout']['Details']['WorkoutName']
      instance.description = instance.raw['Workout']['Details']['WorkoutDescription']
      instance.find_intervals()
      instance.find_workout_items()
      instance.assign_workout_items_to_intervals()
    return instance

#------------------------------------------------------------------------------
  def find_intervals(self):
    il = []
    for row in self.raw['Workout']['intervalData']:
      i = Interval.create(raw=row)
      if i.name != "Workout":
        il.append(i)
    self.intervals = il
    
#------------------------------------------------------------------------------
  def find_workout_items(self):
    wl = []
    for row in self.raw['Workout']['workoutData']:
      w = WorkoutItem.create(raw=row)
      wl.append(w)
    self.workout_items = wl

#------------------------------------------------------------------------------
  def assign_workout_items_to_intervals(self):
    for i in self.intervals:
      for w in self.workout_items:
        i.include(w)

#------------------------------------------------------------------------------
  def dump_xml(self):
  #print(f"{len(interval_list)} intervals and {len(workout_item_list)} workout_items")
    print(f"<workout_file>")
    # header info goes here
    print(f"<name>{self.name}</name>")
    print(f"<author>{self.author}</author>")
    print(f"<category>{self.category}</category>")
    print(f"<sportType>{self.sport}</sportType>")
    print(f"<description><![CDATA[{self.description}]]></description>")
    print(f"<workout>")
    for i in self.intervals:
      i.find_type()
      i.to_xml()
      print(i.xml)
    print(f"</workout></workout_file>")

#------------------------------------------------------------------------------
def main():

  p = ArgumentParser(description="Convert a TrainerRoad workout to a Zwift .zwo file")
  p.add_argument('--verbose', '-v', action='store_const', const=True, help="provide feedback while running")
  p.add_argument('file', help="file to load")
  args = p.parse_args()

  data = {}

  with open(args.file, 'r') as f:
    x = f.read()
    data = ujson.loads(x)

  w = Workout.create(raw=data)
  w.dump_xml()

#===============================================================================
if __name__=='__main__':
  main()
