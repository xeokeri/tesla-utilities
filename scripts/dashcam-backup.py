
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

            number_of_entries_copied = 0

            for entry in os.scandir(source_path):
                if entry.is_file():
                    shutil.copy(entry.path, destination_path)
                if entry.is_dir():
                    next_destination_sub_directory = f"{destination_path}/{entry.name}"

                    if not os.path.exists(next_destination_sub_directory):
                        os.mkdir(next_destination_sub_directory)

                    for sub_entry in os.scandir(entry.path):
                        if sub_entry.is_file():
                            shutil.copy(sub_entry.path, next_destination_sub_directory)
                        else:
                            if self.verbose:
                                print(f"Depth not supported for: {sub_entry.path}")
                else:
                    if self.verbose:
                        print(f"Unknown entry type: {entry}")

                number_of_entries_copied += 1

                if self.verbose:
                    print(f"Copying {entry.path} to {destination_path}")

            if self.verbose:
                print(f"Processed {number_of_entries_copied} entries from {source_path} to {destination_path}")

    def list_contents(self):
        root_directory = self.__root_directory()

        for sub_directory in self.__sub_directories():
            sub_path = f"{root_directory}/{sub_directory}"
            source_path = f"{self.source}/{sub_path}"

            self.__list_contents(source_path, level=1)

    def __list_contents(self, location: str, level: int = 0):
        log_prefix = f"{(' ' * 2) * level}"

        print(f"\n{log_prefix}Listing contents of {location}\n")

        for entry in os.scandir(location):
            entry_name = f"{log_prefix}{entry.name}"

            if entry.is_file() and entry.name.endswith(".mp4"):
                print(f"{entry_name} (File)")
            if entry.is_dir():
                print(f"{entry_name} (Directory)")

                self.__list_contents(entry.path, level + 1)

    def __make_directory_if_not_exist(self, path: str, not_exist_message: str, creation_message: str):
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
    parser.add_argument("--list-only", "-l", help="List devices and directories pending copy from source device(s).", action="store_true")
    parser.add_argument("--destination", "-d", help="Destination directory.")
    parser.add_argument("--verbose", "-v", help="Verbose additional info. Default, disabled.", action="store_true")
    args = parser.parse_args()

    system_mount: str
    destination: str = args.destination
    verbose: bool = args.verbose if args.verbose is not None else False
    should_display_list: bool = args.list_only if args.list_only is not None else False

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
            absolute_path = source_directory.absolute().as_posix()
            dashcam = DashcamBackup(source=absolute_path, destination=destination, verbose=verbose)

            print(f"Checking directory: {absolute_path}")
            print(f"Directory: {absolute_path} is a Tesla Drive")
            print(f"Destination: {destination} is the backup destination")

            if should_display_list:
                dashcam.list_contents()
            else:
                dashcam.run()
