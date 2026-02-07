from pymetasploit3.msfrpc import MsfRpcClient
import json
import os
import traceback

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(PROJECT_PATH, "config", "msfrpc-config.json")

if not os.path.exists(config_file_path):
    print(f"Error: Config file not found at {config_file_path}")
    exit(1)

with open(config_file_path) as f:
    MSFRPC_CONFIG = json.load(f)

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
