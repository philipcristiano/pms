from dingus import Dingus, DingusTestCase

from pms.app import *
import pms.app as mod


class WhenMappingDataSetToJavascriptTimes(DingusTestCase(map_data_set_to_javascript_times)):

    def setup(self):
        super(WhenMappingDataSetToJavascriptTimes, self).setup()
        self.time = Dingus('time')
        self.datum = Dingus('datum')
        self.data = [(self.time, self.datum)]

        self.returned = map_data_set_to_javascript_times(self.data)

    def should_change_datetime_to_epoch_times_1000(self):
        assert self.returned == [
            (mod.to_epoch(self.time) * 1000, self.datum)
        ]
