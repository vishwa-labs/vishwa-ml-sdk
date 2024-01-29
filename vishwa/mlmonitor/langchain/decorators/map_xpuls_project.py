import contextvars
from typing import Optional, Any, Dict


class MapXpulsProject:
    _context: contextvars.ContextVar[Optional[Dict[str, Any]]] = contextvars.ContextVar('telemetry_extra_labels_vars',
                                                                                        default=None)

    def __init__(self, project_id: Optional[str] = None, project_slug: Optional[str] = None):
        if project_id is None and project_slug is None:
            raise ValueError("Both `project_id` and `project_slug` cannot be null")
        self.project_id = project_id
        self.project_slug = project_slug

    def __call__(self, func):
        def wrapped_func(*args, **kwargs):
            self._context.set({'project_id': self.project_id, 'project_slug': self.project_slug})

            return func(*args, **kwargs)

        return wrapped_func
