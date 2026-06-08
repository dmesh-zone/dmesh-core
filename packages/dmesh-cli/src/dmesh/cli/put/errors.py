"""Custom exceptions for dm put commands."""


class DmPutError(Exception):
    """Base exception for dm put errors."""





class FileNotFoundError(DmPutError):
    """The ODPS YAML file at the given path does not exist."""


class YamlParseError(DmPutError):
    """The file at the given path is not valid YAML."""


class DpPublishError(DmPutError):
    """The WS layer returned an error or was unreachable."""
