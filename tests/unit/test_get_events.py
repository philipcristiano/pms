from dingus import Dingus, DingusTestCase

import pms.app as mod
from pms.app import get_events


class WhenGettingEvents(DingusTestCase(get_events)):

    def setup(self):
        super(WhenGettingEvents, self).setup()
        self.query = Dingus()

        self.returned = get_events(self.query)

    def should_query_events(self):
        assert mod.events.calls('find', self.query)

    def should_sort_descending(self):
        assert mod.events.find().calls('sort', '_id', -1)

