#!/bin/bash

if grep -qs '/mnt/central_dogma' /proc/mounts; then
filebot -script fn:amc --action move -non-strict --conflict auto \
	--log-file /opt/renamer/amc.log \
	--output "/mnt/central_dogma" \
	--def plex=localhost:ZLu7q5TrZu6pd8ZX12yz \
	--def @/opt/renamer/amc_args.txt \
	"/mnt/ritsuko/deluge/completed"
fi
