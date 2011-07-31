from dingus import Dingus, DingusTestCase

import pms.app as mod
from pms.app import record


class WhenRecordingEvents(DingusTestCase(record)):

    def setup(self):
        super(WhenRecordingEvents, self).setup()

        self.returned = record()

    def should_json_loads_request_data(self):
        assert mod.json.calls('loads', mod.request.data)

    def should_insert_data_safely(self):
        assert mod.events.calls('insert', mod.json.loads(), safe=True)

    def should_generate_rollups(self):
        assert mod.generate_rollups.calls('()', mod.json.loads())

    def should_return_status(self):
        assert self.returned == mod.jsonify()

    def should_jsonify_status(self):
        assert mod.jsonify.calls('()', {'status': 200})


