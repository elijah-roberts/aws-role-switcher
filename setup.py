from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='aws-role-switcher',
    version='0.4.2',
    py_modules=['aws-role-switcher'],
    author="Elijah Roberts",
    author_email="elijah@elijahjamesroberts.com",
    description="This is a CLI application to switch your role using autocompletion by parsing your config/credential file and set environment variables",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    download_url="https://github.com/elijah-roberts/aws-role-switcher/archive/0.4.2.tar.gz",
    keywords=['AWS', 'ROLE', 'GIT', 'PROFILE', 'AUTOCOMPLETE'],
    packages=find_packages(),
    scripts=['bin/aws-role-switcher.sh', 'bin/aws-role-switcher'],
    install_requires=[
        'prompt_toolkit',
        'setuptools'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)