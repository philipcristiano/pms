from dingus import Dingus, DingusTestCase

import pms.app as mod
from pms.app import next


class WhenGettingNext(DingusTestCase(next)):

    def setup(self):
        super(WhenGettingNext, self).setup()
        self.oid = Dingus('oid')
        self.event = Dingus('event')
        mod.events.find().sort.return_value = [self.event]

        self.returned = next(self.oid)

    def should_wrap_oid_with_object_id(self):
        assert mod.ObjectId.calls('()', self.oid)


class WhenGettingNextAndNoMoreEvents(DingusTestCase(next)):

    def setup(self):
        super(WhenGettingNextAndNoMoreEvents, self).setup()
        self.oid = Dingus('oid')
        mod.events.find().sort.return_value = []

        self.returned = next(self.oid)

    def should_wrap_oid_with_object_id(self):
        assert mod.ObjectId.calls('()', self.oid)


