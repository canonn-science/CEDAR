# coding: utf8
import os
import argparse
import simplejson
from ceddn.conf.Version import __version__ as version
from os.path import join, dirname
from pathlib import Path
from dotenv import load_dotenv
path='/etc/ceddn/.env'
load_dotenv(dotenv_path=path,verbose=True)


class _Settings(object):

    CEDDN_VERSION = version

    ###############################################################################
    # Local installation settings
    ###############################################################################

    CERT_FILE                               = os.getenv("CERT_FILE")
    KEY_FILE                                = os.getenv("KEY_FILE")

    ###############################################################################
    # Relay settings
    ###############################################################################

    RELAY_HTTP_BIND_ADDRESS                 = "0.0.0.0"
    RELAY_HTTP_PORT                         = 9090

    RELAY_RECEIVER_BINDINGS                 = ["tcp://127.0.0.1:8500"]

    RELAY_SENDER_BINDINGS                   = ["tcp://*:9500"]

    # If set to False, no deduplicate is made
    RELAY_DUPLICATE_MAX_MINUTES             = 15

    # If set to false, don't listen to topic and accept all incoming messages
    RELAY_RECEIVE_ONLY_GATEWAY_EXTRA_JSON   = True

    RELAY_EXTRA_JSON_SCHEMAS                = {}

    ###############################################################################
    #  Gateway settings
    ###############################################################################

    GATEWAY_HTTP_BIND_ADDRESS               = "127.0.0.1"
    GATEWAY_HTTP_PORT                       = 8081

    GATEWAY_SENDER_BINDINGS                 = ["tcp://127.0.0.1:8500"]

    GATEWAY_JSON_SCHEMAS                    = {

        "https://ceddn.canonn.tech/schemas/codex/1"         : "schemas/codex-v1.0.json",
        "https://ceddn.canonn.tech/schemas/codex/1/test"    : "schemas/codex-v1.0.json",
        "https://ceddn.canonn.tech/schemas/material/1"         : "schemas/material-v1.0.json",
        "https://ceddn.canonn.tech/schemas/material/1/test"    : "schemas/material-v1.0.json"

    }

    GATEWAY_OUTDATED_SCHEMAS                = []

    ###############################################################################
    #  Monitor settings
    ###############################################################################

    MONITOR_HTTP_BIND_ADDRESS               = "0.0.0.0"
    MONITOR_HTTP_PORT                       = 9091

    MONITOR_RECEIVER_BINDINGS               = ["tcp://127.0.0.1:8500"]

    MONITOR_DB = {
        "host":     os.getenv("MONITOR_DB_HOST"),
        "port":     os.getenv("MONITOR_DB_PORT"),
        "user":     os.getenv("MONITOR_DB_USER"),
        "password": os.getenv("MONITOR_DB_PASS"),
        "database": os.getenv("MONITOR_DB_NAME")
    }

    MONITOR_UA                              = os.getenv("MONITOR_GA_UA")




    def loadFrom(self, fileName):
        f = open(fileName, 'r')
        conf = simplejson.load(f)
        for key, value in conf.iteritems():
            if key in dir(self):
                self.__setattr__(key, value)
            else:
                print "Ignoring unknown setting {0}".format(key)

Settings = _Settings()


def loadConfig():
    '''
    Loads in a settings file specified on the commandline if one has been specified.
    A convenience method if you don't need other things specified as commandline
    options. Otherwise, point the filename to Settings.loadFrom().
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", nargs="?", default=None)
    args = parser.parse_args()

    if args.config:
        Settings.loadFrom(args.config)
