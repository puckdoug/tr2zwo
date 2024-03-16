#!/usr/local/bin/python3

from typing import Dict
import msgspec


# ------------------------------------------------------------------------------
class WorkoutItem(msgspec.Struct):
  verbose: bool = False
  raw: Dict = {}
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
