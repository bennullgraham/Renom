#!env /usr/bin/python
from argparse import ArgumentParser
import re
import shutil

parser = ArgumentParser(
    description='Rename a set of episodes from one numbering scheme to another. Useful in situations where automated processors like Sickbeard don\'t understand a certain scheme and require a rename to s01e01 or 01x01 styles.',
)
# positional
parser.add_argument('extract', help='This is used to understand episode and series information in the files being renamed. It should include special tokens {episode} and {series}, and in the case of files with non-episode digits, enough surrounding text to disambiguate. Example: "Showname - s{series}e{episode}.avi". Note that either token may be missing if --reindex or --series is given.')
parser.add_argument('rename', help='New file naming scheme, e.g. "Showname.-.{series}x{episode}.avi"')
parser.add_argument('files', help='Files to be renamed', nargs='+')

# optional
parser.add_argument('--reindex', metavar='N', help='Discard episode numbers; reindex from this number. If this option is used then the order of filenames given to this program becomes important.', default=False)
parser.add_argument('--series', metavar='N', help='Series number used if missing in episode filename')
parser.add_argument('-x', '--execute', action='store_true', help='Rename files. Otherwise, only perform a dry run.', default=False)

args = parser.parse_args()


class Extractor(object):

    tokens = {
        '{episode}': '(?P<episode>[0-9]+)',
        '{series}': '(?P<series>[0-9]+)',
    }

    def __init__(self, template):
        self.template = template
        self.re = None

    def _regex(self):
        if not self.re:
            self.re = self.template
            for token, replacement in self.tokens.iteritems():
                self.re = self.re.replace(token, replacement)
            self.re = re.compile(self.re)
        return self.re

    def extract(self, string):
        return self._regex().search(string)


class Episode(object):

    def __init__(self, filename_orig, rename_pattern, series_position=False):
        self.filename_orig = filename_orig
        self.filename_new = None
        self.rename_pattern = rename_pattern
        self.numbering = {}
        self.series_position = series_position

    def parse_filename(self, extractor):
        parsed = extractor.extract(self.filename_orig)
        if not parsed:
            raise Exception('Couldn\'t pull info from filename "%s" (trying to match with "%s")' % (self.filename_orig, extractor.template))
        for k, n in parsed.groupdict().iteritems():
            self.numbering[k] = n.zfill(2)
        if args.reindex:
            self.numbering['episode'] = str(self.series_position + int(args.reindex)).zfill(2)
        if not self.numbering['episode']:
            raise Exception('Episode number not found in filename and not reindexing (try --reindex if no episode information in filenames)')

    def apply_rename(self):
        self.filename_new = self.rename_pattern.format(**self.numbering)

    def move(self):
        pass
        shutil.move(self.filename_orig, self.filename_new)


class Series(object):

    def __init__(self, filenames, number=None):
        self.number = number
        self.episodes = []
        self.extractor = Extractor(args.extract)
        self._from_filenames(filenames)

        if self.number:
            self.number = self.number.zfill(2)
        else:
            raise Exception("Series not found in filename and not manually provided (try --series)")

    def _from_filenames(self, filenames):
        for f in filenames:
            e = Episode(
                filename_orig=f,
                rename_pattern=args.rename,
                series_position=len(self.episodes)
            )
            e.parse_filename(self.extractor)
            e.apply_rename()
            # override this series' number if an episode has another idea
            if 'series' in e.numbering and e.numbering['series']:
                self.number = e.numbering['series']
            self.episodes.append(e)

    def preview(self):
        from_width = max(map(lambda e: len(e.filename_orig), self.episodes))
        to_width = max(map(lambda e: len(e.filename_new), self.episodes))

        print 'Here\'s the plan:\n'
        print 'Original Filename'.ljust(from_width), '    ', 'New Filename'.ljust(to_width)
        print ''.join(['-' for n in range(0, from_width + to_width + 6)])
        for ep in self.episodes:
            print colour(ep.filename_orig.ljust(from_width) + ' -> ' + ep.filename_new.ljust(to_width), 'blue')
        print "\nArgue " + colour('--execute', 'green') + " to perform renaming"

    def rename(self):
        for ep in self.episodes:
            ep.move()


def colour(msg, colour):
    def c(colour):
        prefix = '\033['
        colour_map = {
            'black':   '30m',
            'blue':    '34m',
            'yellow':  '33m',
            'cyan':    '36m',
            'green':   '32m',
            'magenta': '35m',
            'red':     '31m',
            'white':   '37m',
            'reset':   '0m'
        }
        return prefix + colour_map[colour]
    return c(colour) + msg + c('reset')


def main():
    if not args.extract:
        raise Exception("--extract argument is required")

    if not args.rename:
        raise Exception("--rename argument is required")

    if not args.files:
        raise Exception("No filenames given for renaming")

    s = Series(filenames=args.files, number=args.series)
    if args.execute:
        s.rename()
    else:
        s.preview()


try:
    main()
except Exception, ex:
    print colour('Fatal: ', 'red') + ex.message
