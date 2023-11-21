from xpuls.mlmonitor.langchain.decorators.map_xpuls_project import MapXpulsProject
from xpuls.mlmonitor.langchain.decorators.telemetry_override_labels import TelemetryOverrideLabels


def get_scoped_override_labels():
    try:
        override_labels = TelemetryOverrideLabels._context.get()
        if override_labels is None:
            override_labels = {}
    except Exception as e:
        override_labels = {}
    return override_labels


def get_scoped_project_info():
    try:
        project_details = MapXpulsProject._context.get()
        if project_details is None:
            project_details = {'project_id': 'default'}
    except Exception as e:
        project_details = {'project_id': 'default'}
    return project_details
