# Dwell Clicker

A simple tool that simulates a mouse click if the cursor remains stationary for a predetermined amount of time. This project is useful for users looking for accessibility options or those who need automated clicking solutions.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background

Dwell Clicker is designed to help individuals who may have difficulty with manual clicking or anyone who can benefit from automatic clicking after a dwell period. This script uses Python and the `pynput` library to monitor mouse movement and clicks, triggering a click action when the mouse has been still for a set amount of time.

## Install

This project uses Python and `pynput`. Go to Python's [website](https://python.org) to download and install Python. Installation of `pynput` is managed through pip.

```sh
pip install pynput
```

Ensure you have Python and pip installed prior to installing the `pynput` library.

## Usage

To run Dwell Clicker, you need to have Python installed on your system as well as the `pynput` library. Save the script as `dwell_clicker.py`.

Run the script in your terminal or command prompt:

```sh
python dwell_clicker.py
```

By default, the dwell time is set to 2 seconds. You can adjust the dwell time by changing the `dwell_time` variable inside the script.

### Controls

- **Move Mouse**: Resets the dwell timer.
- **Manual Click**: Cancels the automatic click if performed before the dwell timer finishes.

### Stopping the Script

To stop the dwell clicker, simply interrupt the process by pressing `Ctrl+C` in your terminal or command prompt.

## Maintainers

[@swiftcast](https://github.com/swiftcast).

## Contributing

Feel free to dive in! [Open an issue](https://github.com/swiftcast/dwell-clicker/issues/new) or submit PRs.

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
Standard Readme adheres to the [Contributor Covenant](https://contributor-covenant.org/version/2/0/code_of_conduct/) code of conduct.
