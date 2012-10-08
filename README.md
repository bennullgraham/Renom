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
$ ./Renom.py 'Showname s{series} episode {episode}.avi' 'Mightypants season {series} episode {episode}.avi' *.avi
```

2. 
```bash
$ ~/rename.py --series=3 'Showname {episode} of 12.avi' 'Terrible Badger {series}x{episode}.avi' *.avi
```

