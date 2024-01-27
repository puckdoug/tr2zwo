# tr2zwo

A python package to convert TrainerRoad workouts into Zwift ZWO format custom workout files. This allows TrainerRoad
subscribers to easily follow their TrainerRoad plan in the Zwift world.

## installation

```shell
$ python -m pip install tr2zwo
```

## Usage
```shell
$ tr2zwift -h
usage: tr2zwift [-h] [--verbose] {setup,fetch} ...

Convert a TrainerRoad workout to a Zwift .zwo file

positional arguments:
  {setup,fetch}
    setup        initial setup, can be run again to update settings
    fetch        fetch a workout

options:
  -h, --help     show this help message and exit
  --verbose, -v  provide feedback while running

 $ tr2zwift setup -h
 usage: tr2zwift setup [-h] [--username USERNAME] [--password PASSWORD] [--directory DIRECTORY]

 options:
   -h, --help            show this help message and exit
   --username USERNAME, -u USERNAME
                         Your TrainerRoad username
   --password PASSWORD, -p PASSWORD
                         Your TrainerRoad password
   --directory DIRECTORY, -d DIRECTORY
                         Output directory for .zwo file s

$ tr2zwift fetch -h
usage: tr2zwift fetch [-h] [--print] url [url ...]

positional arguments:
  url          The URL(s) of the trainerroad workout(s) to fetch

options:
  -h, --help   show this help message and exit
  --print, -p  Print the zwo to stdout, does not write file

  ```

## References

[ZWO Tag Reference]( https://github.com/h4l/zwift-workout-file-reference/blob/master/zwift_workout_file_tag_reference.md)
