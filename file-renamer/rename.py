import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parents[0]
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")
CONFIG = json.load(open(CONFIG_FILE))

parser = argparse.ArgumentParser()
parser.add_argument("scan_dir")
parser.add_argument("-a", "--action", choices=["move", "copy", "test"], default="move")
parser.add_argument("-c", "--conflict", choices=["auto", "skip", "override"], default="auto")
args = parser.parse_args()
scan_path = Path(args.scan_dir).resolve()

if not os.path.isdir(scan_path):
    sys.exit("Scan path is not a directory: {}".format(scan_path))

if not os.path.isdir(CONFIG['output']['dir']):    
    sys.exit("Output dir is not a directory: {}".format(CONFIG['output']['dir']))

if CONFIG['output']['isMount'] and not os.path.ismount(CONFIG['output']['dir']):
    sys.exit("Output dir is not mounted: {}".format(CONFIG['output']['dir']))

print("Scanning dir: '{}'; Action: '{}'; Conflict strategy: '{}'".format(scan_path, args.action, args.conflict))

AMC_OPTIONS = {"--def {}={}".format(k,v) for (k,v) in CONFIG['amc']['options'].items()}

CMD_ARGS = [
    "filebot",
    "-script fn:amc",
    "--action {}".format(args.action),
    "--conflict {}".format(args.conflict),
    "-non-strict",
    "--log-file {logDir}".format(**CONFIG),
    "--def plex={host}:{token}".format(**CONFIG['plex']),
    " ".join(AMC_OPTIONS),
    str(scan_path)
]
subprocess.run(CMD_ARGS)
