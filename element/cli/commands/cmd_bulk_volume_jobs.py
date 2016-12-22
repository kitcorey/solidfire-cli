#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright &copy; 2014-2016 NetApp, Inc. All Rights Reserved.
#
# DO NOT EDIT THIS CODE BY HAND! It has been generated with jsvcgen.
#

import click

from element.cli import utils as cli_utils
from element.cli.cli import pass_context
from element.solidfire_element_api import SolidFireRequestException
from element import utils
import jsonpickle
import json

@click.group()
@pass_context
def cli(ctx):
    """Account methods."""
    ctx.sfapi = ctx.client

@cli.command('list', short_help="ListBulkVolumeJobs")
@pass_context
def list(ctx):
    """ListBulkVolumeJobs is used to return information about each bulk volume read or write operation that is occurring in the system."""
    ListBulkVolumeJobsResult = ctx.element.list_bulk_volume_jobs()
    cli_utils.print_result(ListBulkVolumeJobsResult, as_json=ctx.json, depth=ctx.depth, filter_tree=ctx.filter_tree)

