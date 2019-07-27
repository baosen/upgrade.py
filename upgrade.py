#!/usr/bin/env python3
import os
import psutil
import sys

# Check if upgrade is running.
def isrunning():
    count = 0
    for pid in psutil.pids():
        p = psutil.Process(pid) # TODO: Race condition bug here when program exits when called, then the pid does not exists anymore.
        if p.name() == "upgrade.py":
            count = count + 1
    return count > 1

# Check if the lock that hinders pacman to run twice simultanously in parallell is set.
def islocked():
    return os.path.isfile("/var/lib/pacman/db.lck");

# Check if upgrade is running.
if isrunning():
    sys.exit("upgrade is currently running. Aborting...")

# Check if lock is set in /var/lib/pacman/db.lck.
if islocked():
    sys.exit("pacman is currently running. Aborting...")

# Upgrade system with the newest packages.
os.system("yaourt -Syu --aur --noconfirm")
