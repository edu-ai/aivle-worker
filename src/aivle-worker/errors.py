class DotEnvFileNotFound(Exception):
    pass


class MissingDotEnvField(Exception):
    pass


class QueueInfoNotFound(Exception):
    pass


class StopConsumingError(Exception):
    pass


class ResumeConsumingError(Exception):
    pass
