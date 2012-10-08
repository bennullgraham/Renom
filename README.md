Usage
-----

    Renom.py [-h] [--reindex N] [--series N] [-x]
                extract rename files [files ...]

Rename a set of episodes from one numbering scheme to another. Useful in
situations where automated processors like Sickbeard don't understand a
certain scheme and require a rename to s01e01 or 01x01 styles.

```
positional arguments:
  extract        This is used to understand episode and series information in
                 the files being renamed. It should include special tokens
                 {episode} and {series}, and in the case of files with non-
                 episode digits, enough surrounding text to disambiguate.
                 Example: "Showname - s{series}e{episode}.avi". Note that
                 either token may be missing if --reindex or --series is
                 given.
  rename         New file naming scheme, e.g.
                 "Showname.-.{series}x{episode}.avi"
  files          Files to be renamed

optional arguments:
  -h, --help     show this help message and exit
  --reindex N    Discard episode numbers; reindex from this number. If this
                 option is used then the order of filenames given to this
                 program becomes important.
  --series N     Series number used if missing in episode filename
  -x, --execute  Rename files. Otherwise, only perform a dry run.
```

Examples
--------

1.  
```bash
$ ls -1
Showname s01 episode 1 of 7.avi
Showname s01 episode 2 of 7.avi
Showname s01 episode 3 of 7.avi
Showname s01 episode 4 of 7.avi
Showname s01 episode 5 of 7.avi
Showname s01 episode 6 of 7.avi
Showname s01 episode 7 of 7.avi

$ ./Renom.py 's{series} episode {episode}' 'Showname {series}x{episode}.avi' *.avi
Here's the plan:

Original Filename                    New Filename      
-------------------------------------------------------
Showname s01 episode 1 of 7.avi -> Showname 01x01.avi
Showname s01 episode 2 of 7.avi -> Showname 01x02.avi
Showname s01 episode 3 of 7.avi -> Showname 01x03.avi
Showname s01 episode 4 of 7.avi -> Showname 01x04.avi
Showname s01 episode 5 of 7.avi -> Showname 01x05.avi
Showname s01 episode 6 of 7.avi -> Showname 01x06.avi
Showname s01 episode 7 of 7.avi -> Showname 01x07.avi

Argue --execute to perform renaming

$ ./Renom.py 's{series} episode {episode}' 'Showname {series}x{episode}.avi' *.avi --execute
$ ls -1
Showname 01x01.avi
Showname 01x02.avi
Showname 01x03.avi
Showname 01x04.avi
Showname 01x05.avi
Showname 01x06.avi
Showname 01x07.avi
```

2.  
```bash
# here the series is specified because it isn't present in the filename
$ ./Renom.py --series=3 'Showname {episode} of 12.avi' 'Terrible Badger {series}x{episode}.avi' *.avi
```

Patterns
--------

 - Internally, the `{episode}` and `{series}` tokens are expanded into named regular expression subgroups: `(?P<episode>[0-9]+)`.
 - The extract pattern doesn't need to match the entire filename, only enough of it to ensure the correct part is matched.