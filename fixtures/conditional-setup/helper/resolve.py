import json
with open("helper/sources.json") as f:
    print(json.load(f)["installer_url"])
