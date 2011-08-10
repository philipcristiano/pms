from configobj import ConfigObj

local_config = ConfigObj('dev.conf')
system_config = ConfigObj('/etc/pms/pms.conf')

config = {}
config.update(system_config)
config.update(local_config)

for name, rollup_config in config['aggregation'].items():
    if type(rollup_config['properties']) != list:
        rollup_config['properties'] = [rollup_config['properties']]
