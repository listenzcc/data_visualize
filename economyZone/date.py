# File: date.py
# Aim: Date manager
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Date(object):
    # Date object for stamp date string
    def __init__(self,
                 date='2020-01-01',
                 interval=relativedelta(months=1),
                 config={}):
        # -----------------------------------------------
        # date: the init date;
        # interval: option of how long the interval is,
        #           self.next method uses it;
        # config: the local config object.
        if config.has_section('Environment'):
            section = config['Environment']
        else:
            section = dict()

        iD = [int(e) for e in section.get('initData', date).split('-')]
        self.date = datetime(iD[0], iD[1], iD[2])

        interval = section.get('interval', interval)
        table = dict(
            monthly=relativedelta(months=1),
            daily=relativedelta(days=1),
            yearly=relativedelta(years=1)
        )
        if interval in table:
            self.interval = table[interval]
        else:
            self.interval = interval

        # -----------------------------------------------
        # Generate weekdays and monthnames,
        # weekday: [Xxx] short name of weekday,
        # monthname: [Xxx] short name of month.
        self.weekdays = calendar.weekheader(4).split()
        self.monthnames = calendar.month_abbr

    def next(self):
        # Move forward as self.interval
        self.date += self.interval

    def forward(self, step=None):
        # Move forward as customized [step]
        if step is None:
            self.next()
        else:
            self.date += step

    def string(self):
        # Return the string of current date
        split = dict(
            weekday=self.weekdays[self.date.weekday()],
            month=self.monthnames[self.date.month],
            day=self.date.day,
            year=self.date.year,
        )
        return '{weekday}, {month}, {day}, {year}'.format(**split)
