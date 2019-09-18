import click
from click.testing import CliRunner
from element.cli import cli
from element.cli.utils import encrypt
import os
import csv
from pkg_resources import Requirement, resource_filename

# For the connection commands we set it up so that the sdk returns a fake connection.
def check_functionality_of_connection_suite():
    runner = CliRunner()
    # First run the push
    result = runner.invoke(cli.cli, ["connection", "push", '--mvip', "10.117.61.44", "--username", "admin", "--password", "admin", "--name", "b"])
    # Next, verify that it happened by opening up the csv file and checking.

    connectionsCsvLocation = resource_filename(Requirement.parse("solidfire-cli"), "connections.csv")
    with open(connectionsCsvLocation) as connectionFile:
        connections = list(csv.DictReader(connectionFile, delimiter=','))

    assert connections[-1]["mvip"] == "10.117.61.44"
    assert connections[-1]["username"] == str(encrypt("admin"))
    assert connections[-1]["password"] == str(encrypt("admin"))
    assert connections[-1]["name"] == "b"
    print("Push is working")

    result = runner.invoke(cli.cli, ["connection", "remove", "--name", "b"])
    with open(connectionsCsvLocation) as connectionFile:
        connections = list(csv.DictReader(connectionFile, delimiter=','))
    connectionsNamedb = [connection for connection in connections if connection["name"] == "b"]
    assert len(connectionsNamedb) == 0
    print("Remove is working")
    print("Functionality is good")

check_functionality_of_connection_suite()
