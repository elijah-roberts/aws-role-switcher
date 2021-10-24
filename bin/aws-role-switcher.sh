#!/bin/sh
if [[ $* == *-h* ]]; then
  aws-role-switcher $@
elif [[ $* == *-v* ]]; then
    aws-role-switcher $@
else
  eval "$(aws-role-switcher "$@")"
fi