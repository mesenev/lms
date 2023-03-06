# -*- python -*-
# ex: set filetype=python:
import os

import dotenv
from buildbot.plugins import *


dotenv.load_dotenv('home/buildbot/buildbot.env')
c = BuildmasterConfig = dict()
c['buildbotNetUsageData'] = 'basic'
repository_url = 'https://github.com/mesenev/lms.git'

c['workers'] = [
    worker.Worker("lms-worker-main", "pass"),
    worker.Worker("lms-worker-force", "pass"),
    worker.Worker("lms-worker-production", "pass"),
]

main_factory = util.BuildFactory()
main_factory.addStep(steps.Git(repourl=repository_url, mode='incremental'))
main_factory.addStep(steps.ShellCommand(command=[
    'cp', '/home/buildbot/bb-lms/worker-main/buildscript.py', '../buildscript.py'
]))
main_factory.addStep(steps.ShellCommand(command=['cp', '/home/buildbot/settings.py', 'imcslms/settings.py']))
main_factory.addStep(steps.ShellCommand(command=['cp', '/home/buildbot/common.env', '.docker/conf/common.env']))
main_factory.addStep(steps.ShellCommand(command=['python', '../buildscript.py']))

production_factory = util.BuildFactory()
production_factory.addStep(steps.Git(repourl=repository_url, mode='full'))
production_factory.addStep(steps.ShellCommand(command=[
    'cp', '/home/buildbot/bb-lms/worker-production/buildscript.py', '../buildscript.py'
]))
production_factory.addStep(steps.ShellCommand(command=['cp', '/home/buildbot/prod_settings.py', 'imcslms/settings.py']))
production_factory.addStep(
    steps.ShellCommand(command=['cp', '/home/buildbot/prod_common.env', '.docker/conf/common.env']))
production_factory.addStep(steps.ShellCommand(command=['python', '../buildscript.py']))

c['builders'] = [
    util.BuilderConfig(name="lmsci", workernames=["lms-worker-main"], factory=main_factory),
    util.BuilderConfig(name="lmsforce", workernames=["lms-worker-force"], factory=main_factory),
    util.BuilderConfig(name="lmsprod", workernames=["lms-worker-production"], factory=production_factory),
]

c['protocols'] = {'pb': {'port': 9989}}
c['change_source'] = [
    changes.GitPoller(repository_url, workdir='/home/buildbot/workdir-develop', branches=['develop'], pollInterval=40),
    changes.GitPoller(repository_url, workdir='/home/buildbot/workdir-master', branches=['master'], pollInterval=40),
]

c['schedulers'] = [
    schedulers.SingleBranchScheduler(
        name="develop",
        treeStableTimer=5 * 60,
        change_filter=util.ChangeFilter(branch='develop'),
        builderNames=["lmsci"]),
    schedulers.SingleBranchScheduler(
        name="master",
        change_filter=util.ChangeFilter(category='pull'),
        builderNames=["lmsprod"]),
    schedulers.ForceScheduler(
        name="force",
        builderNames=["lmsforce"])
]

c['title'] = "lms ci system"
c['titleURL'] = "mesenev/lms"

c['buildbotURL'] = os.getenv("BUILDBOT_ADDRESS", "http://localhost:8010/")
c['www'] = dict(
    port="tcp:8010:interface=localhost",
    plugins=dict(
        waterfall_view={},
        console_view={},
        grid_view={},
        profiler=True,
        badges=dict(left_pad=0, right_pad=0, border_radius=3, style="badgeio"),
    )
)
c['db'] = {'db_url': "sqlite:///state.sqlite", }
