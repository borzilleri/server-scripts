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
parser.add_argument("scan", nargs="?", help="Base dir to scan for media.")
parser.add_argument("-s", "--scan-mount", dest="scan_mount", action="store_true", help="Set this if the scan dir should be checked to see if it's mounted. This is ignored if the default scan dir is used.")

parser.add_argument("-o", "--output", help="Base dir to write files to.")
parser.add_argument("-m", "--output-mount", dest="output_mount", action="store_true", help="Set this if the ouput dir should be checked to see if it's mounted. This is ignored if --output is not also specified.")

parser.add_argument("-a", "--action", choices=["move", "copy", "test"], default="move")
parser.add_argument(
    "-c", "--conflict", choices=["auto", "skip", "override"], default="auto"
)
args = parser.parse_args()

def check_dir(label: str, path: str, mount: bool) -> Path:
    if not os.path.isdir(path):
        sys.exit("{} dir is not a directory: {}".format(label, path))
    if mount and not os.path.ismount(path):
        sys.exit("{} dir is not mounted: {}".format(label, path))
    return Path(path).resolve()

scan_dir = check_dir("Scan", args.scan if args.scan else CONFIG['input']['dir'], args.scan_mount if args.scan else CONFIG['input']['isMount'])
output_dir = check_dir("Output", args.output if args.output else CONFIG['output']['dir'], args.output_mount if args.output else CONFIG['output']['isMount'])

print(
    "Scanning: {}; Output: {}; Action: '{}'; Conflict strategy: '{}'".format(
        scan_dir, output_dir, args.action, args.conflict
    ),
    flush=True,
)

FILEBOT_OPTIONS = [
    "-script fn:amc",
    "--action {}".format(args.action),
    "-non-strict",
    "--conflict {}".format(args.conflict),
    "--output {}".format(output_dir),
    "--def @{}".format(CONFIG["amc"]["options"]),
]
CMD = "{exe} {opts} {dir}".format(exe=CONFIG['filebot']['path'], opts=" ".join(FILEBOT_OPTIONS), dir=scan_dir)
print("Running shell command: '{}'".format(CMD), flush=True)
subprocess.run(CMD, shell=True)
