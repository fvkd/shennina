#!/usr/bin/env python3
import json
import os
from pymetasploit3.msfrpc import MsfRpcClient

# Base config
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
SCANS_PATH = os.path.join(PROJECT_PATH, ".scans/")
REPORTS_PATH = os.path.join(PROJECT_PATH, "reports/")

# Second brain configuration
SUPERVISOD_CSV_FILE = os.path.join(PROJECT_PATH, 'data/exploits.csv')
SECOND_BRAIN_NAME = 'second_brain'

if not os.path.exists(SCANS_PATH):
    os.mkdir(SCANS_PATH)
if not os.path.exists(REPORTS_PATH):
    os.mkdir(REPORTS_PATH)

EXPLOITS_TREE_PATH = os.path.join(PROJECT_PATH, "data", "exploits_tree.json")

EXFILTRATION_SERVER = os.environ.get("EXFILTRATION_SERVER", "127.0.0.1:8040")
LHOST = os.environ.get("LHOST", "127.0.0.1")
MAX_TESTING_THREADS = 10
SCANNING_THROUGH_TEST = False
TTL_FOR_EXPLOIT_VALIDATION = 15.0

# Cache Search Results
CACHED_SEARCH_RESULTS = {}

# Exploits Tree & Array
EXPLOITS_TREE = {}
EXPLOITS_ARRAY = []
EXPLOITS_SET = set()





# Functions
def getClient():
    config_path = os.path.join(PROJECT_PATH, "config", "msfrpc-config.json")
    if not os.path.exists(config_path):
        return None

    try:
        with open(config_path) as f:
            MSFRPC_CONFIG = json.load(f)

        client = MsfRpcClient(MSFRPC_CONFIG["password"],
                              username=MSFRPC_CONFIG["user"],
                              host=MSFRPC_CONFIG["host"],
                              port=MSFRPC_CONFIG["port"],
                              ssl=MSFRPC_CONFIG["ssl"])
        return client
    except Exception as e:
        print(f"Error connecting to MSF RPC: {e}")
        return None


def loadExploitsTree(detailed=True):
    if not os.path.exists(EXPLOITS_TREE_PATH):
        return {} if detailed else []
    exploits_tree = json.loads(open(EXPLOITS_TREE_PATH, "r").read())
    if detailed:
        return {e['exploit']: e for e in exploits_tree}
    return [_['exploit'] for _ in exploits_tree]


def get_exploits_tree():
    global EXPLOITS_TREE
    if not EXPLOITS_TREE and os.path.exists(EXPLOITS_TREE_PATH):
        EXPLOITS_TREE = loadExploitsTree()
    return EXPLOITS_TREE


def get_os_list():
    tree = get_exploits_tree()
    os_set = set()
    # Handle both list (legacy) and dict (optimized) formats
    entries = tree.values() if isinstance(tree, dict) else tree
    for exploit_entry in entries:
        exploit_path = exploit_entry.get('exploit', '')
        parts = exploit_path.split('/')
        if parts:
            os_set.add(parts[0])
    return sorted(list(os_set))


def get_service_list():
    tree = get_exploits_tree()
    service_set = set()
    # Handle both list (legacy) and dict (optimized) formats
    entries = tree.values() if isinstance(tree, dict) else tree
    for exploit_entry in entries:
        exploit_path = exploit_entry.get('exploit', '')
        parts = exploit_path.split('/')
        if len(parts) >= 3:
            service_set.add(parts[1])
    return sorted(list(service_set))
