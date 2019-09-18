import click
from click.testing import CliRunner
from element.cli import cli
import jsonpickle
import random
import os
import csv
from solidfire.models import *
from unittest.mock import MagicMock

def rand_string(length):
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(length))

def check_strange_inputs():
    # First, make a new account. Set the CHAPSecret to confirm that CHAPSecrets work. This exercises a CHAPSecret parameter
    runner = CliRunner()
    result = runner.invoke(cli.cli, ["connection", "push", '--mvip', "10.117.61.44", "--username", "admin", "--password", "admin", "--name", "b"])
    account_name = rand_string(15)
    result = runner.invoke(cli.cli, ['-c','0','-j',"account", "add", '--username', account_name, '--initiatorsecret', "solidfire1234"])
    account = jsonpickle.decode(result.output)["result"]
    account_id = account["accountID"]
    result = runner.invoke(cli.cli, ['-c','0','-j',"account", "getbyid", '--accountid', account_id])
    fullAccount = jsonpickle.decode(result.output)["result"]

    # Verify that CHAPSecret is working.
    assert fullAccount["account"]["initiatorSecret"] == "solidfire1234"

    # Next, make two volumes
    result = runner.invoke(cli.cli, ['-c','0','-j',"volume", "create", '--name', rand_string(15), "--accountid", account_id, "--totalsize", "1000000000", "--enable512e", True])
    volume1 = jsonpickle.decode(result.output)["result"]
    result = runner.invoke(cli.cli, ['-c','0','-j',"volume", "create", '--name', rand_string(15), "--accountid", account_id, "--totalsize", "1000000000", "--enable512e", True])
    volume2 = jsonpickle.decode(result.output)["result"]

    # Now we modify the QoS settings on Volume1 in order to test the functionality of a complex param type:
    result = runner.invoke(cli.cli, ['-c','0','-j',"volume", "modify", '--volumeid', volume1["volumeID"], '--miniops', 100])

    # Now we get the volumes from the given account to make sure they're there and that the QoS Change took.:
    result = runner.invoke(cli.cli, ['-c','0','-j',"volume", "list", '--accounts', str(account_id)])
    volumes_list = jsonpickle.decode(result.output)["result"]
    assert len(volumes_list["volumes"]) == 2
    newVolume1 = [volume for volume in volumes_list["volumes"] if volume["volumeID"] == volume1["volumeID"]][0]
    assert newVolume1["qos"]["minIOPS"] == 100

    # Now we delete and purge them. This exercises the use of an array.
    for volume_id in (str(volume1["volumeID"]), str(volume2["volumeID"])):
        result = runner.invoke(cli.cli, ['-c','0','-j',"volume", "delete", '--volumeid', volume_id])
        result = runner.invoke(cli.cli, ['-c','0','-j',"volume", "purgeDeleted", '--volumeid', volume_id])

    # Finally, we check to make sure they're gone.
    result = runner.invoke(cli.cli, ['-c','0','-j',"volume", "list", '--accounts', str(account_id)])
    volumes_list = jsonpickle.decode(result.output)["result"]
    assert len(volumes_list["volumes"]) == 0

    # Now tear down the account.
    result = runner.invoke(cli.cli, ['-c','0','-j',"account", "Remove", '--accountid', account_id])

    # Now, to test a supercomplex parameter, we need to make a volume access group and set the attributes via json:
    result = runner.invoke(cli.cli, ['-c','0','-j',"volumeaccessgroup","create","--name", "DISPOSABLE", '--attributes', '{\"blah\":\"blah\"}'])
    volume_access_group = jsonpickle.decode(result.output)["result"]
    assert volume_access_group["volumeAccessGroup"]["attributes"]["blah"] == "blah"
    result = runner.invoke(cli.cli, ['-c','0','-j',"volumeaccessgroup", "delete", '--volumeaccessgroupid', volume_access_group["volumeAccessGroupID"]])
    result = runner.invoke(cli.cli, ["connection", "remove", "--name", "b"])


check_strange_inputs()
