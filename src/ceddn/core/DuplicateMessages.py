# coding: utf8
import hashlib
import re
import simplejson

from datetime import datetime, timedelta
from ceddn.conf.Settings import Settings
from threading import Lock, Thread
from time import sleep


class DuplicateMessages(Thread):
    max_minutes = Settings.RELAY_DUPLICATE_MAX_MINUTES

    caches = {}

    lock = Lock()

    def __init__(self):
        super(DuplicateMessages, self).__init__()
        self.daemon = True

    def run(self):
        while True:
            sleep(60)
            with self.lock:
                maxTime = datetime.utcnow()

                for key in self.caches.keys():
                    if self.caches[key] + timedelta(minutes=self.max_minutes) < maxTime:
                        del self.caches[key]

    def isDuplicated(self, json):
        with self.lock:
            # Test messages are never duplicate, would be a pain to wait for another test :D
            if re.search('test', json['$schemaRef'], re.I):
                return False

            # Shallow copy, minus headers
            jsonTest = {
                '$schemaRef': json['$schemaRef'],
                'message': dict(json['message']),
            }

            # Remove timestamp (Mainly to avoid multiple scan messages and faction influences)
            jsonTest['message'].pop('timestamp')

            # Ensure most duplicate messages will get the same key
            message = simplejson.dumps(jsonTest, sort_keys=True)
            key = hashlib.sha256(message).hexdigest()

            if key not in self.caches:
                self.caches[key] = datetime.utcnow()
                return False
            else:
                self.caches[key] = datetime.utcnow()
                return True
