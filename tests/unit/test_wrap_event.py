from dingus import Dingus, DingusTestCase

import pms.app as mod
from pms.app import wrap_event


class WhenWrappingEvent(DingusTestCase(wrap_event)):

    def setup(self):
        super(WhenWrappingEvent, self).setup()
        self.event = Dingus('event')

        wrap_event(self.event)

    def should_not_fail(self):
        pass
