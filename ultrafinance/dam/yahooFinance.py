'''
Created on Dec 21, 2010

@author: ppa

Thanks to Corey Goldberg, this module is based http://www.goldb.org/ystockquote.html
sample usage:
>>> import YahooFinance
>>> print YahooFinance.get_price('GOOG')
529.46
'''
import urllib
import traceback
from ultrafinance.model import Quote
from ultrafinance.lib.errors import UfException, Errors

import logging
LOG = logging.getLogger()

class YahooFinance(object):
    def __request(self, symbol, stat):
        try:
            url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, stat)
            return urllib.urlopen(url).read().strip().strip('"')
        except IOError:
            raise UfException(Errors.NETWORK_ERROR, "Can't connect to Yahoo server")
        except BaseException:
            raise UfException(Errors.UNKNOWN_ERROR, "Unknown Error in YahooFinance.__request %s" % traceback.format_exc())

    def getAll(self, symbol):
        """
        Get all available quote data for the given ticker symbol.
        Returns a dictionary.
        """
        values = self.__request(symbol, 'l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7').split(',')
        data = {}
        data['price'] = values[0]
        data['change'] = values[1]
        data['volume'] = values[2]
        data['avg_daily_volume'] = values[3]
        data['stock_exchange'] = values[4]
        data['market_cap'] = values[5]
        data['book_value'] = values[6]
        data['ebitda'] = values[7]
        data['dividend_per_share'] = values[8]
        data['dividend_yield'] = values[9]
        data['earnings_per_share'] = values[10]
        data['52_week_high'] = values[11]
        data['52_week_low'] = values[12]
        data['50day_moving_avg'] = values[13]
        data['200day_moving_avg'] = values[14]
        data['price_earnings_ratio'] = values[15]
        data['price_earnings_growth_ratio'] = values[16]
        data['price_sales_ratio'] = values[17]
        data['price_book_ratio'] = values[18]
        data['short_ratio'] = values[19]
        return data

    def getQuotes(self, symbol, start, end):
        """
        Get historical prices for the given ticker symbol.
        Date format is 'YYYY-MM-DD'

        Returns a nested list.
        """
        try:
            start = str(start).replace('-', '')
            end = str(end).replace('-', '')

            url = 'http://ichart.yahoo.com/table.csv?s=%s&' % symbol + \
                'd=%s&' % str(int(end[4:6]) - 1) + \
                'e=%s&' % str(int(end[6:8])) + \
                'f=%s&' % str(int(end[0:4])) + \
                'g=d&' + \
                'a=%s&' % str(int(start[4:6]) - 1) + \
                'b=%s&' % str(int(start[6:8])) + \
                'c=%s&' % str(int(start[0:4])) + \
                'ignore=.csv'
            days = urllib.urlopen(url).readlines()
            values = [day[:-2].split(',') for day in days]
            # sample values:[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Clos'], \
            #              ['2009-12-31', '112.77', '112.80', '111.39', '111.44', '90637900', '109.7']...]
            data = []
            for value in values[1:]:
                data.append(Quote(value[0], value[1], value[2], value[3], value[4], value[5], value[6]))

            dateValues = sorted(data, key = lambda q: q.time)
            return dateValues

        except IOError:
            raise UfException(Errors.NETWORK_ERROR, "Can't connect to Yahoo server")
        except BaseException:
            raise UfException(Errors.UNKNOWN_ERROR, "Unknown Error in YahooFinance.getHistoricalPrices %s" % traceback.format_exc())
        #sample output
        #[stockDaylyData(date='2010-01-04, open='112.37', high='113.39', low='111.51', close='113.33', volume='118944600', adjClose='111.6'))...]