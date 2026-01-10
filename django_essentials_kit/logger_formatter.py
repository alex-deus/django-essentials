import logging

from json_log_formatter import VerboseJSONFormatter

from django.conf import settings
from django.utils import timezone

__all__ = ['JSONFormatter']


class JSONFormatter(VerboseJSONFormatter):
    def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
        if "request" in extra:
            del extra["request"]

        extra["level"] = record.levelname
        extra["name"] = record.name
        extra["message"] = message

        branch = getattr(settings, "BRANCH", None)
        if branch:
            extra["branch"] = branch

        commit = getattr(settings, "COMMIT", None)
        if commit:
            extra["commit"] = commit

        if "time" not in extra:
            extra["time"] = timezone.now()

        if record.exc_info:
            extra["exc_info"] = self.formatException(record.exc_info)

        return extra
