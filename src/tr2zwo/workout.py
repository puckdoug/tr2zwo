#!/usr/local/bin/python3

import ujson
import msgspec
from typing import List, Dict
from tr2zwo.workoutitem import WorkoutItem
from tr2zwo.interval import Interval

#------------------------------------------------------------------------------
class Workout(msgspec.Struct):
  raw: Dict = None
  verbose: bool = False
  author: str = 'TrainerRoad'
  name: str = None
  description: str = None
  category: str = 'TrainerRoad'
  #subcategory: str = ''
  sport: str = 'bike'
  intervals: List[Interval] = []
  workout_items: List[WorkoutItem] = []
  zwo: str = ''

#------------------------------------------------------------------------------
  @classmethod
  def create(cls, **kwargs):
    instance = Workout()
    if 'raw' in kwargs:
      instance.raw = kwargs['raw']
      instance.name = instance.raw['Workout']['Details']['WorkoutName']
      instance.description = \
        instance.raw['Workout']['Details']['WorkoutDescription']
  #    instance.subcategory = instance.raw['Workout']['Details']['Zones']['Description']
      instance.find_workout_items()
      instance.find_intervals()
      instance.build_zwo()
    return instance

#------------------------------------------------------------------------------
  def find_workout_items(self):
    wi = []
    for row in self.raw['Workout']['workoutData']:
      w = WorkoutItem.create(raw=row)
      wi.append(w)
    self.workout_items = wi

#------------------------------------------------------------------------------
  def find_intervals(self):
    il = []
    for row in self.raw['Workout']['intervalData']:
      i = Interval.create(raw=row)
      if i.name != "Workout":
        i.assign_workout_items(self.workout_items)
        #for w in self.workout_items:
          #i.include(w)
        #i.find_type()
        #i.to_xml()
        il.append(i)
    self.intervals = il

#------------------------------------------------------------------------------
  def add(self, row):
    self.zwo = self.zwo + row + '\n'

#------------------------------------------------------------------------------
  def build_zwo(self):
    self.add("<workout_file>")
    # header info goes here
    self.add(f"<name>{self.name}</name>")
    self.add(f"<activitySaveName>TrainerRoad: {self.name}</activitySaveName>")
    self.add(f"<author>{self.author}</author>")
    self.add(f"<category>{self.category}</category>")
    #if self.subcategory:
      #f.write(f"<subcategory>{self.subcategory}</subcategory>")
    self.add(f"<sportType>{self.sport}</sportType>")
    self.add(f"<description><![CDATA[{self.description}]]></description>")
    self.add("<workout>")
    for i in self.intervals:
      self.add(i.xml)
    self.add("</workout>")
    self.add("</workout_file>")

#------------------------------------------------------------------------------
  def write(self, directory='.'):
    filename = f"{directory}/{self.name}.zwo"
    if self.verbose:
      print(f"filename: {filename}")
    with open(filename, 'w') as f:
      f.write(self.zwo)

#------------------------------------------------------------------------------
  def print(self):
    print(self.zwo)

#------------------------------------------------------------------------------
def main():
  pass


#===============================================================================
if __name__ == '__main__':
  main()
