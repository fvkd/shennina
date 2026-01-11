from pymetasploit3.msfrpc import MsfRpcClient
import json
import os
import traceback

PROJECT_PATH = "/home/getfucked/projects/shennina"
MSFRPC_CONFIG = open(PROJECT_PATH + "/config/" + "msfrpc-config.json")
MSFRPC_CONFIG = json.loads(MSFRPC_CONFIG.read())

print(f"Connecting to {MSFRPC_CONFIG['host']}:{MSFRPC_CONFIG['port']} as {MSFRPC_CONFIG['user']}...")
try:
    # Use username instead of user for pymetasploit3
    client = MsfRpcClient(MSFRPC_CONFIG["password"],
                          username=MSFRPC_CONFIG["user"],
                          host=MSFRPC_CONFIG["host"],
                          port=MSFRPC_CONFIG["port"],
                          ssl=MSFRPC_CONFIG["ssl"])
    print("Success!")
    print(f"Modules: {len(client.modules.exploits)}")
except Exception as e:
    print(f"Failed: {e}")
    traceback.print_exc()