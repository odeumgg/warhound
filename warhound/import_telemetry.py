from warhound import event
import simplejson as json


class ImportTelemetry:
    def __init__(self, path):
        self.path = path


    def __call__(self):
        with open(self.path, 'rb') as telemetry_file:
            output = json.loads(telemetry_file.read())
            output = sorted(output, key=lambda json: json['cursor'])
            output = list(map(event.json_object_to_event, output))

            assert type(output) is list

            return (output,)


def mk(*args, **kwargs):
    return ImportTelemetry(*args, **kwargs)
