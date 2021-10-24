#!/usr/bin/env python3

import configparser
import os
from pathlib import Path

from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.validation import Validator

REGIONS = [
    "eu-north-1",
    "ap-south-1",
    "eu-west-3",
    "eu-west-2",
    "eu-west-1",
    "ap-northeast-2",
    "ap-northeast-1",
    "sa-east-1",
    "ca-central-1",
    "ap-southeast-1",
    "ap-southeast-2",
    "eu-central-1",
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2"
]

AWS_VARS = ["AWS_SECRET_ACCESS_KEY", "AWS_ACCESS_KEY_ID", "AWS_SESSION_TOKEN", "AWS_SECURITY_TOKEN"]


class ARS:

    def __init__(self):
        self.config = configparser.ConfigParser()
        default_path = os.path.join(Path.home(), '.aws/credentials')
        extended_path = os.environ.get('AWS_PROFILE_SWITCHER_PATH')
        if extended_path:
            path = extended_path
        else:
            path = default_path
        self.config.read(path)

    def run(self, sys_args):
        self.__init__()
        profile_arg, region_arg = self.parse_arguments(sys_args)
        self.set_aws_vars(profile_arg)
        current_region = os.environ.get("AWS_DEFAULT_REGION", None)
        if current_region:
            if region_arg:
                if region_arg not in [current_region, current_region.replace("-","")]:
                    self.set_aws_region(region_arg)
        else:
            self.set_aws_region(region_arg)


    def set_aws_vars(self, arg):
        validator = Validator.from_callable(
            self.profile_validator,
            error_message='Not a valid profile name',
            move_cursor_to_end=True)
        if self.profile_validator(arg):
            profile = arg
        else:
            profile = prompt('Enter Profile: ',
                            default=arg,
                            completer=FuzzyWordCompleter(self.config.sections()),
                            complete_while_typing=True,
                            validator=validator)

        for k, v in self.config[profile].items():
            if k.upper() in AWS_VARS:
                print(f"export {k.upper()}={v}")

    def profile_validator(self, text):
        if text in self.config.sections():
            return True
        else:
            return False

    @staticmethod
    def set_aws_region(arg):
        region = prompt('AWS_DEFAULT_REGION Not Set. Choose Region: ', default=arg,
                        completer=FuzzyWordCompleter(REGIONS))
        print(f"export AWS_DEFAULT_REGION={region}")

    @staticmethod
    def region_validator(text):
        if text in REGIONS:
            return True
        else:
            return False

    @staticmethod
    def parse_arguments(sys_args):
        if len(sys_args) <= 1:
            return "", ""
        elif len(sys_args) == 2:
            return sys_args[1], ""
        else:
            return sys_args[1], sys_args[2]
