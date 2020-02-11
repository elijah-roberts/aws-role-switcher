# aws_role_switcher

This is a CLI application makes it easier to switch roles using auto completion from parsing your aws config/credential file and setting `"AWS_SECRET_ACCESS_KEY", "AWS_ACCESS_KEY_ID", "AWS_SESSION_TOKEN"` environment variables if present.

This script does not support MFA roles, and designed to help cycle through profiles set manually, or as output from an SSO script like: https://github.com/Nike-Inc/gimme-aws-creds
## Installation
```python3 -m pip install -U aws_role_switcher```

In order to work properly this script must be sourced, add the following to your .profile or .bashrc( you can adjust the alias name to whatever you want)
```alias ars='source aws-role-switcher.sh'```

Note: You can run this from the command line using `. aws-role-switcher.sh` or `source aws-role-switcher.sh`.

## Configuration
You can set the following environmental variables:

`AWS_PROFILE_SWITCHER_PATH` - Override the default credential/config file location from `$HOME/.aws/credentials`
 
 I would recommend adding to your ~/.profile or ~/.bash_profile
 


## Example Usage

`ars` to start prompt. TAB or start typing to start auto completion list. TAB or use arrows to cycle through list, and enter to select.

Example config file:

```
[default]
aws_access_key_id = REDACTED
aws_secret_access_key = redacted
aws_session_token = default

[testing-administrator]
aws_access_key_id = REDACTED
aws_secret_access_key = redacted
aws_session_token = testing

[staging-administrator]
aws_access_key_id = REDACTED
aws_secret_access_key = redacted
aws_session_token = staging

[production-administrator]
aws_access_key_id = REDACTED
aws_secret_access_key = redacted
aws_session_token = production
```

Example Usage:

![AWS Role Switcher Demo](examples/aws-switch-roles.gif)


 ## Development

### Bug Reports & Feature Requests

Please use the submit a issue to report any bugs or file feature requests.

### Developing

If you are interested in being a contributor and want to get involved in developing this CLI application feel free to reach out

In general, PRs are welcome. We follow the typical trunk based development Git workflow.

 1. **Branch** the repo 
 2. **Clone** the project to your own machine
 3. **Commit** changes to your branch
 4. **Push** your work back up to your branch
 5. Submit a **Merge/Pull Request** so that we can review your changes

**NOTE:** Be sure to merge the latest changes from "upstream" before making a pull request!
