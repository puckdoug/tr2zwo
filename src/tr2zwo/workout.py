#!/usr/local/bin/python3

import ujson
import msgspec
from typing import List, Dict
from tr2zwo.workoutitem import WorkoutItem
from tr2zwo.interval import Interval

#------------------------------------------------------------------------------
class Workout(msgspec.Struct):
  verbose: bool = False
  raw: Dict = None
  zwo: str = ''
  author: str = 'TrainerRoad'
  name: str = None
  description: str = None
  goaldescription: str = None
  category: str = 'TrainerRoad'
  subcategory: str = ''
  sport: str = 'bike'
  url: str = ''
  intervals: List[Interval] = []
  workout_items: List[WorkoutItem] = []

#------------------------------------------------------------------------------
  @classmethod
  def create(cls, **kwargs):
    instance = Workout()
    if 'url' in kwargs:
      instance.url = kwargs['url']
    if 'raw' in kwargs:
      instance.raw = kwargs['raw']
      try:
        instance.name = instance.raw['Workout']['Details']['WorkoutName']
      except:
        pass
      try:
        instance.description = \
          instance.raw['Workout']['Details']['WorkoutDescription']
      except:
        pass
      try:
        instance.goaldescription = \
          instance.raw['Workout']['Details']['GoalDescription']
      except:
        pass
      try:
        instance.subcategory = \
          instance.raw['Workout']['Details']['Progression']['Text']
      except:
        pass
      instance.find_workout_items()
      instance.find_intervals()
      instance.build_zwo()
    return instance

#------------------------------------------------------------------------------
  def find_workout_items(self):
    workout_item_list = []
    for row in self.raw['Workout']['workoutData']:
      w = WorkoutItem.create(raw=row)
      workout_item_list.append(w)
    self.workout_items = workout_item_list

#------------------------------------------------------------------------------
  def find_intervals(self):
    interval_list = []
    for row in self.raw['Workout']['intervalData']:
      i = Interval.create(raw=row)
      if i.name != "Workout":
        i.assign_workout_items(self.workout_items)
        interval_list.append(i)
    self.intervals = interval_list

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
    if self.subcategory:
      self.add(f"<subcategory>{self.subcategory}</subcategory>")
    self.add(f"<sportType>{self.sport}</sportType>")

    desc = f"""<description><![CDATA[
    {self.description}

    {self.goaldescription}

    URL: {self.url}
    ]]></description>"""

    self.add(desc)

    # workout data
    self.add("<workout>")
    for i in self.intervals:
      self.add(i.xml)
    self.add("</workout>")

    # close
    self.add("</workout_file>")

#------------------------------------------------------------------------------
  def write(self, directory='.'):
    filename = f"{directory}/{self.name}.zwo"
    if self.verbose:
      print(f"filename: {filename}")
    with open(filename, 'w') as f:
      f.write(self.zwo)

#------------------------------------------------------------------------------
  def print_raw(self):
    print(ujson.dumps(self.raw, indent=2))

#------------------------------------------------------------------------------
  def print(self):
    print(self.zwo)

#------------------------------------------------------------------------------
def main():
  pass

#===============================================================================
if __name__ == '__main__':
  main()
