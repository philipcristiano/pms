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
####
##
## generate_rollup
##
####

class WhenGeneratingASingleRollup(DingusTestCase(generate_rollup)):

    def setup(self):
        super(WhenGeneratingASingleRollup, self).setup()
        self.event = {
            '_id': Dingus('_id'),
            'prop_1': Dingus('prop_1'),
            'prop_2': Dingus('prop_2'),
        }
        self.name = Dingus('name')
        self.properties = ['prop_1', 'prop_2']

        generate_rollup(self.event, self.name, self.properties)

    def should_upsert_rollup(self):
        call = mod.rollups.calls[0]
        opts = call[1]
        calldoc = opts[0]
        update_doc = opts[1]
        doc = {
            'date': {
                'year': self.event['_id'].generation_time.year,
                'month': self.event['_id'].generation_time.month,
                'day': self.event['_id'].generation_time.day,
            },
            'name': self.name,
            'properties': {
                'prop_1': self.event['prop_1'],
                'prop_2': self.event['prop_2'],
            }
        }
        update = {
            '$inc': {
                'data.total' : 1,
                'data.hour.{0.hour}'.format(self.event['_id'].generation_time): 1,
                'data.minute.{0.hour}:{0.minute}'.format(self.event['_id'].generation_time): 1,
            }
        }
        eq_(calldoc, doc)
        eq_(update_doc, update)
        assert mod.rollups.calls('update', doc, update, upsert=True)


class WhenGeneratingASingleRollupAndEventDoesntMatch(DingusTestCase(generate_rollup)):

    def setup(self):
        super(WhenGeneratingASingleRollupAndEventDoesntMatch, self).setup()
        self.event = {
            '_id': Dingus('_id'),
            'prop_1': Dingus('prop_1'),
        }
        self.name = Dingus('name')
        self.properties = ['prop_1', 'prop_2']

        generate_rollup(self.event, self.name, self.properties)

    def should_not_upsert_rollup(self):
        assert not mod.rollups.calls('update')
