
#!/usr/bin/env python3

"""dashcam-backup.py: Backup Tesla DashCam to a backup drive."""

__author__      = "Xeon Xai"
__copyright__   = "Copyright © 2024, Xeon Xai"
__credits__     = ["Xeon Xai"]
__maintainer__  = "Xeon Xai"
__description__ = "Backup Tesla DashCam to a backup drive."
__date__        = "2024-01-01"
__license__     = "BSD 3-Clause License"
__version__     = "1.0.0"

import os, platform, shutil
import argparse

from pathlib import Path
from typing import List

class DashcamBackup:
    """This script is used to backup the USB Tesla DashCam drives to a backup drive. Currently supports MacOS and Linux."""

    def __init__(self, source: str, destination: str, verbose: bool = False):
        self.source = source
        self.destination = destination
        self.verbose = verbose

    def run(self):
        root_directory = self.__root_directory()

        if self.verbose:
            print(f"Backing up from {self.source} to {self.destination}")

        for sub_directory in self.__sub_directories():
            sub_path = f"{root_directory}/{sub_directory}"
            source_path = f"{self.source}/{sub_path}"
            destination_path = f"{self.destination}/{sub_path}"

            self.__make_directory_if_not_exist(source_path, not_exist_message=f"Source path {source_path} does not exist", creation_message=f"Creating source path {source_path}")
            self.__make_directory_if_not_exist(destination_path, not_exist_message=f"Destination path {destination_path} does not exist", creation_message=f"Creating destination path {destination_path}")

            if self.verbose:
                print(f"Processing {sub_directory} from {self.source} to {self.destination}")

            number_of_entries_copied: int = 0

            for entry in os.scandir(source_path):
                if entry.is_file():
                    shutil.copy(entry.path, destination_path)
                if entry.is_dir():
                    shutil.copytree(entry.path, destination_path)
                else:
                    if self.verbose:
                        print(f"Unknown entry type: {entry}")

                number_of_entries_copied += 1

                if self.verbose:
                    print(f"Copying {entry.path} to {destination_path}")

            if self.verbose:
                print(f"Processed {number_of_entries_copied} entries from {source_path} to {destination_path}")

    def __make_directory_if_not_exist(self, path: str, not_exist_message: str = None, creation_message: str = None):
        if not os.path.exists(path):
            if not_exist_message is not None:
                print(not_exist_message)
            else:
                print(f"Directory {path} does not exist")

            os.mkdir(path)

            if creation_message is not None:
                print(creation_message)
            else:
                print(f"Created directory {path}")

    def __sub_directories(self) -> List[str]:
        return [
            "RecentClips",
            "SavedClips",
            "SentryClips",
        ]

    def __root_directory(self) -> str:
        return "TeslaCam"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup Tesla Dashcam")
    parser.add_argument("--destination", "-d", help="Destination directory.")
    parser.add_argument("--verbose", "-v", help="Verbose additional info. Default, disabled.", action="store_true")
    args = parser.parse_args()

    system_mount: str = None
    destination: str = args.destination
    verbose: bool = args.verbose if args.verbose is not None else False

    if destination is None:
        print("Destination is required")
        exit(1)
    elif not os.path.exists(destination):
        print(f"Destination {destination} does not exist")
        exit(1)

    match platform.system():
        case "Linux":
            system_mount = "/mnt"
        case "Darwin":
            system_mount = "/Volumes"
        case "Windows":
            print("Running on Windows, not supported.")
        case _:
            print("Running on an unknown system, not supported.")

    if system_mount is None:
        print("System mount is not set, exiting.")
        exit(1)
    else:
        print(f"System mount is set to {system_mount}")

        system_path = Path(system_mount)

        source_directories = [
            item_path for item_path in system_path.iterdir()
            if item_path.is_dir()
            if item_path.name.startswith("TESLADRIVE")
        ]

        for source_directory in source_directories:
            print(f"Directory: {source_directory} is a Tesla Drive")
            print(f"Destination: {destination} is the backup destination")

            dashcam = DashcamBackup(source=source_directory, destination=destination, verbose=verbose)
            dashcam.run()
