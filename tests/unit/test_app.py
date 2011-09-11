from dingus import Dingus, DingusTestCase

from nose.tools import eq_
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


class WhenMappingDataSetToLocalTime(DingusTestCase(map_dataset_to_local_time)):

    def setup(self):
        super(WhenMappingDataSetToLocalTime, self).setup()
        self.time = Dingus('time')
        self.datum = Dingus('datum')
        self.data = [(self.time, self.datum)]

        self.returned = map_dataset_to_local_time(self.data, 120)

    def should_adust_time(self):
        assert self.returned == [
            (self.time + mod.datetime.timedelta(), self.datum)
        ]

    def should_create_timedelta(self):
        assert mod.datetime.calls('timedelta', minutes=120)


####
##
## index
##
####

class WhenGettingIndexPage(DingusTestCase(index)):

    def setup(self):
        super(WhenGettingIndexPage, self).setup()

        self.returned = index()

    def should_render_template(self):
        assert mod.render_template.calls('()',
            'graph.jinja2',
            config=mod.config
        )

    def should_return_rendered_template(self):
        assert self.returned == mod.render_template()


####
##
## flatten
##
####

class WhenFlattening(object):

    def setup(self):
        self.data = Dingus('data')

        self.returned = flatten(self.data)

    def should_create_new_dict(self):
        for key in self.data:
            eq_(self.returned[key], self.data[key])


####
##
## generate_rollups
##
####

class WhenGeneratingRollups(DingusTestCase(generate_rollups)):

    def setup(self):
        super(WhenGeneratingRollups, self).setup()
        self.name = Dingus('name')
        self.rollup_config = Dingus('rollup_config')
        self.rollups = {self.name: self.rollup_config}
        mod.config['aggregation'] = self.rollups
        self.event = Dingus('event')

        generate_rollups(self.event)

    def should_generate_rollups(self):
        for name, rollup_config in mod.config['aggregation'].items():
            assert mod.generate_rollup.calls('()',
                self.event,
                self.name,
                self.rollup_config['properties']
            )
