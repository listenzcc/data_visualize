# File: date.py
# Aim: Date manager
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta

from . import logger


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
        if isinstance(config, dict):
            section = dict()
            logger.warning(
                'Config is not provided, using default initialization.')
        else:
            if config.has_section('Environment'):
                section = config['Environment']
            else:
                section = dict()
                logger.warning(
                    'Config has no "Environment" section, using default initialization.')

        iD = [int(e) for e in section.get('initDate', date).split('-')]
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

        logger.debug('Date initialized as date: {}, interval: {}'.format(self.string(),
                                                                         self.interval))

    def next(self):
        # Move forward as self.interval
        self.date += self.interval
        logger.debug('Date moved forward as {}'.format(self.interval))

    def forward(self, step=None):
        # Move forward as customized [step]
        if step is None:
            self.next()
        else:
            self.date += step
            logger.debug('Date moved forward as {}'.format(step))

    def string(self):
        # Return the string of current date
        split = dict(
            stamp=self.date.timestamp(),
            weekday=self.weekdays[self.date.weekday()],
            month=self.monthnames[self.date.month],
            day=self.date.day,
            year=self.date.year,
        )
        return '{stamp}, {weekday}, {month}, {day}, {year}'.format(**split)
