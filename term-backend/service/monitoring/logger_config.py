from structlog.typing import EventDict, WrappedLogger


class ColorRenderer:
    def __call__(self, logger: WrappedLogger, name: str, event_dict: EventDict) -> EventDict:  # noqa: ARG002
        record = event_dict["_record"]
        event_dict["thread_name"] = record.threadName
        event_dict["process_name"] = record.processName
        return event_dict
