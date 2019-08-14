# coding: utf8

import simplejson
import strict_rfc3339
from enum import IntEnum
from jsonschema import validate as jsValidate, ValidationError, FormatChecker


class Validator(object):

    schemas = {"http://example.com": {}}

    def addSchemaResource(self, schemaRef, schema):
        if schemaRef in self.schemas.keys():
            raise Exception("Attempted to redefine schema for " + schemaRef)
        schema = simplejson.loads(schema)
        self.schemas[schemaRef] = schema

    def validate(self, json_object):
        results = ValidationResults()

        if "$schemaRef" not in json_object:
            results.add(ValidationSeverity.FATAL, JsonValidationException("No $schemaRef found, unable to validate."))
            return results

        schemaRef = json_object["$schemaRef"]
        if schemaRef not in self.schemas.keys():
            #  We don't want to go out to the Internet and retrieve unknown schemas.
            results.add(ValidationSeverity.FATAL, JsonValidationException("Schema " + schemaRef + " is unknown, unable to validate."))
            return results

        schema = self.schemas[schemaRef]
        try:
            jsValidate(json_object, schema, format_checker=FormatChecker())
        except ValidationError as e:
            results.add(ValidationSeverity.ERROR, e)

        return results


class ValidationSeverity(IntEnum):
    OK = 0,
    WARN = 1,
    ERROR = 2,
    FATAL = 3


class ValidationResults(object):

    def __init__(self):
        self.severity = ValidationSeverity.OK
        self.messages = []

    def add(self, severity, exception):
        self.severity = max(severity, self.severity)
        self.messages.append(exception)


class JsonValidationException(Exception):
    pass
