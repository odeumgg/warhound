import os
import simplejson as json
import sys

# Run this example from your project root.
cwd = os.getcwd()
sys.path.append(cwd)

import warhound

# For your usage: Change this to a path to a telemetry.
telemetry_path = os.path.join(cwd, 'telemetries', 'my_telemetry.json')

with open(telemetry_path, 'rb') as telemetry:
    raw = telemetry.read()
    warhound.process(json.loads(raw))
