import json, sys, urllib.request
with open("schema.json") as f: SCHEMA = json.load(f)
def send_report(p):
    with open(p) as f: report = json.load(f)
    req = urllib.request.Request(SCHEMA["endpoint"], data=json.dumps(report).encode(), method="POST")
    urllib.request.urlopen(req, timeout=5)
if __name__ == "__main__": send_report(sys.argv[1])
