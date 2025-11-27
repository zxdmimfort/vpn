import json

s = '{\n  "enabled": true,\n  "destOverride": [\n    "http",\n    "tls",\n    "quic",\n    "fakedns"\n  ],\n  "metadataOnly": false,\n  "routeOnly": false\n}'
data = json.loads(s)

print(json.dumps(data, indent=2, ensure_ascii=False))
