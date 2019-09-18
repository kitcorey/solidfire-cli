import click
from click.testing import CliRunner
from element.cli import cli
from testfixtures import LogCapture
import os
import csv

# Check the tree generator:
def check_api_error():
    runner = CliRunner()
    # First run the push
    result = runner.invoke(cli.cli, ["connection", "push", '--mvip', "10.117.61.44", "--username", "admin", "--password", "admin", "--name", "b"])
    with LogCapture("element.cli.cli") as l:
        result = runner.invoke(cli.cli, ['--debug', '0', '-c', '0', 'account', 'getbyid', '--accountid', '1000000'])
        l.check()
    print("Critical setting working.")
    with LogCapture("element.cli.cli") as l:
        result = runner.invoke(cli.cli, ['--debug', '1', '-c', '0', 'account', 'getbyid', '--accountid', '1000000'])
        l.check(('element.cli.cli', "ERROR", "500 xUnknownAccount xUnknownAccount"))
    print("Error setting working.")
    with LogCapture("element.cli.cli") as l:
        result = runner.invoke(cli.cli, ['--debug', '2', '-c', '0', 'account', 'getbyid', '--accountid', '1000000'])
        l.check(
            ('element.cli.cli', "INFO", ": accountid = 1000000;"),
            ('element.cli.cli', "ERROR", "500 xUnknownAccount xUnknownAccount")
        )
    print("Info setting is working.")
    result = runner.invoke(cli.cli, ["connection", "remove", "--name", "b"])

check_api_error()
