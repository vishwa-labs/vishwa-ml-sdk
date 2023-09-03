import contextvars
from typing import Optional, Any, Dict


class TelemetryOverrideLabels:
    _context: contextvars.ContextVar[Optional[Dict[str, Any]]] = contextvars.ContextVar('telemetry_extra_labels_vars',
                                                                                        default=None)

    def __init__(self, **labels):
        self.labels = labels

    def __call__(self, func):
        def wrapped_func(*args, **kwargs):
            self._context.set(self.labels)
            return func(*args, **kwargs)

        return wrapped_func
