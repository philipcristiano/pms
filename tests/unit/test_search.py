from dingus import Dingus, DingusTestCase

import pms.app as mod
from pms.app import search


class WhenGettingSearch(DingusTestCase(search)):

    def setup(self):
        super(WhenGettingSearch, self).setup()

        self.returned = search()

    def should_flatten_request_args(self):
        assert mod.flatten.calls('()', mod.request.args)

    def should_get_events(self):
        assert mod.get_events.calls('()', mod.flatten())

    def should_jsonify_events(self):
        assert mod.jsonify.calls('()', {'events': mod.get_events()})
