Python Monitoring Server
========================

Currently under active development. It aims to be a generic solution for
logging events and creating aggregate reports.

Installing Development Environment
----------------------------------

    git clone git://github.com/philipcristiano/pms.git

    cd pms

    make bootstrap && make deploy


Deploying PMS
-------------

PMS can be deployed as a WSGI app. Once installed the app is available
as ``pms.app:app`` and can be run with gunicorn or a WSGI server of your
choice.

Configuration
-------------

PMS will look for a config file at ``/etc/pms/pms.conf``

You config file would look something like this:

    [mongodb]
    host=33.33.33.10

    [aggregation]
        [[host-level]]
            properties=host,level
        [[random]]
            properties=level

You need to define a host for Mongo.

The aggregration properties are to define the rollups.  The second level is the
name of the rollup and properties is a list of fields to rollup. PMS will
attempt to rollup any events added. The event will be rolled up if it has
properties matching the set defined for a rollup.
