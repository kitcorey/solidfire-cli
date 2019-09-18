from click.testing import CliRunner

from element.cli import cli


# For the connection commands we set it up so that the sdk returns a fake connection.
def schedule_modify_suite():
    runner = CliRunner()
    # First run the push
    result = runner.invoke(cli.cli, ["connection", "push", '-m', "10.117.61.44", "-u", "admin", "-p", "admin", "-n", "10.117.61.44"])
    assert result.exit_code == 0


    result = runner.invoke(cli.cli, ["-n", "10.117.61.44", "schedule", "modify", "--scheduleid", 48, "--recurring", False])
    assert result.exit_code == 0

    result = runner.invoke(cli.cli, ["connection", "remove", "-n", "10.117.61.44"])

schedule_modify_suite()
