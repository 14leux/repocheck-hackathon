import json, platform
def collect_diagnostics():
    return {"os": platform.system(), "tool_version": "1.4.2", "commands_run_this_session": 12}
if __name__ == "__main__":
    print(json.dumps(collect_diagnostics()))
