import datetime

from dingus import Dingus, DingusTestCase

from pms.aggregates import *
import pms.aggregates as mod


class WhenGettingHourlyDataFromAggregate(DingusTestCase(get_hourly_data_from_aggregate)):

    def setup(self):
        super(WhenGettingHourlyDataFromAggregate, self).setup()
        self.aggregate = Dingus('aggregate')
        mod.int = Dingus('int', return_value=4)

        self.returned = get_hourly_data_from_aggregate(self.aggregate)

    def should_create_date_from_aggregate(self):
        assert mod.datetime.calls(
            'datetime',
            self.aggregate['date']['year'],
            self.aggregate['date']['month'],
            self.aggregate['date']['day'],
        )

    def should_create_timedelta_for_hour(self):
        for hour in self.aggregate['data']['hour']:
            assert mod.datetime.calls('timedelta', hours=mod.int(hour))


    def should_return_list_of_tuples(self):
        for hour in self.aggregate['data']['hour']:
            hour_delta = datetime.timedelta()
            value_dt = mod.datetime.datetime() + hour_delta
            value = self.aggregate['data']['hour'][hour]
            assert self.returned[0] == (value_dt, value)


class WhenGeneratingEmptyDataSet(object):

    def setup(self):
        self.start = datetime.datetime(2011, 8, 1)
        self.stop = datetime.datetime(2011, 8, 3)
        self.interval = datetime.timedelta(hours=1)

        self.returned = generate_empty_data_set(self.start, self.stop, self.interval)

    def should_start_with_start_time(self):
        assert self.returned[0] == (self.start, 0)

    def should_end_with_stop(self):
        assert self.returned[-1] == (self.stop, 0)

    def should_have_second_element(self):
        assert self.returned[1] == (self.start + self.interval, 0)

    def should_have_second_to_last_element(self):
        assert self.returned[-2] == (self.stop - self.interval, 0)


class WhenMergingDataIntoEmptyDataSet(object):

    def setup(self):
        self.empty = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
        self.data = [(1, 1), (3, 1)]

        self.returned = merge_data_into_empty_data_set(self.data, self.empty)

    def should_return_filled_in_data_set(self):
        print self.returned
        assert self.returned == [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)]
