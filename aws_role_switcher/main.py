#!/usr/bin/env python3

import configparser
import os
from pathlib import Path

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion, FuzzyCompleter
from prompt_toolkit.output.color_depth import ColorDepth
from prompt_toolkit.shortcuts import CompleteStyle, prompt
from prompt_toolkit.validation import Validator


from typing import Callable, Dict, Iterable, List, Optional, Pattern, Union

from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from prompt_toolkit.document import Document

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
        if not os.environ.get("AWS_DEFAULT_REGION"):
            self.set_aws_region(region_arg)


    def set_aws_vars(self, arg):
        validator = Validator.from_callable(
            self.profile_validator,
            error_message='Not a valid profile name',
            move_cursor_to_end=True)
        cmpltr = WordCompleter(self.config.sections())
        profile = prompt('Enter Profile: ',
                         default=arg,
                         completer=FuzzyCompleter(cmpltr),
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
                        completer=FuzzyCompleter())
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


class ProfileCompleter(Completer):
    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        for profile in self.config.sections():
            if profile.startswith(word):
                yield Completion(
                    profile,
                    start_position=-len(word),
                    style="fg:" + "red",
                    selected_style="fg:white bg:" + "red",
                )


class WordCompleter(Completer):
    """
    Simple autocompletion on a list of words.
    :param words: List of words or callable that returns a list of words.
    :param ignore_case: If True, case-insensitive completion.
    :param meta_dict: Optional dict mapping words to their meta-text. (This
        should map strings to strings or formatted text.)
    :param WORD: When True, use WORD characters.
    :param sentence: When True, don't complete by comparing the word before the
        cursor, but by comparing all the text before the cursor. In this case,
        the list of words is just a list of strings, where each string can
        contain spaces. (Can not be used together with the WORD option.)
    :param match_middle: When True, match not only the start, but also in the
                         middle of the word.
    :param pattern: Optional compiled regex for finding the word before
        the cursor to complete. When given, use this regex pattern instead of
        default one (see document._FIND_WORD_RE)
    """

    def __init__(
        self,
        words: Union[List[str], Callable[[], List[str]]],
        ignore_case: bool = False,
        meta_dict: Optional[Dict[str, str]] = None,
        WORD: bool = False,
        sentence: bool = False,
        match_middle: bool = True,
        pattern: Optional[Pattern[str]] = None,
    ) -> None:

        assert not (WORD and sentence)

        self.words = words
        self.ignore_case = ignore_case
        self.meta_dict = meta_dict or {}
        self.WORD = WORD
        self.sentence = sentence
        self.match_middle = match_middle
        self.pattern = pattern

    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        # Get list of words.
        words = self.words
        if callable(words):
            words = words()

        # Get word/text before cursor.
        if self.sentence:
            word_before_cursor = document.text_before_cursor
        else:
            word_before_cursor = document.get_word_before_cursor(
                WORD=self.WORD, pattern=self.pattern
            )

        if self.ignore_case:
            word_before_cursor = word_before_cursor.lower()

        def get_color(word: str):
            if "administrator" in word:
                return "red"
            if "breakglass" in word:
                return "red"
            return "gray"

        def word_matches(word: str) -> bool:
            """ True when the word before the cursor matches. """
            if self.ignore_case:
                word = word.lower()

            if self.match_middle:
                return word_before_cursor in word
            else:
                return word.startswith(word_before_cursor)

        for a in words:
            if word_matches(a):
                display_meta = self.meta_dict.get(a, "")
                yield Completion(a, -len(word_before_cursor), display_meta=display_meta, style=f"fg:whitea bg:{get_color(a)}")