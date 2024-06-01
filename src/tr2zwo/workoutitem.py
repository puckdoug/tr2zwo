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
      instance.seconds = instance.raw['Seconds']
      instance.ftp = instance.raw['FtpPercent']
      instance.member_ftp = instance.raw['MemberFtpPercent']
    return instance
