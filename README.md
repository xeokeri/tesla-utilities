# Tesla Utilities

Scripts to improve data management, and backups, of Tesla DashCam footage.

# Usage

python3 scripts/dashcam-backup.py --destination="/Volumes/PathToDestinationBackDriveHere" --verbose

Example: python3 scripts/dashcam-backup.py --destination="/Volumes/TeslaDashCamBackups" --verbose

# Notes

Any mounted USB devices that are prefixed with "TESLADRIVE" will all be backed up in sequence. The script should be able to find them dynamically.

Example: "/Volumes/TESLADRIVE", "/Volumes/TESLADRIVE 1", "/Volumes/TESLADRIVE 2"

# Help

-d, --destination = Destination to the backup drive, where the videos from the Tesla USB drives will be stored.

-l, --list-only = List the contents that are pending to be backed up. Will no copy when this flag is added.

-v, --verbose = Verbose output turned to 11, if present. Default: off.

-h, --help = Show help message.

# Pending

Add more features in the near term, as needed.

# OS Support

Currently supports MacOS and Linux systems.
