from dingus import Dingus, DingusTestCase

import pms.app as mod
from pms.app import to_epoch


class WhenConvertingToEpochTime(DingusTestCase(to_epoch)):

    def setup(self):
        super(WhenConvertingToEpochTime, self).setup()
        self.datetime = Dingus('datetime')

        self.returned = to_epoch(self.datetime)

    def should_make_epoch_time(self):
        assert mod.time.calls('mktime', self.datetime.timetuple())

    def should_return_time(self):
        assert self.returned == mod.time.mktime()
