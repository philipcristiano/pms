from dingus import Dingus, DingusTestCase

import pms.app as mod
from pms.app import listen


class WhenGettingListen(DingusTestCase(listen)):

    def setup(self):
        super(WhenGettingListen, self).setup()

        self.returned = listen()

    def should_get_events(self):
        assert mod.get_events.calls('()')

    def should_jsonify_events(self):
        assert mod.jsonify.calls('()', {'events': mod.get_events()})
