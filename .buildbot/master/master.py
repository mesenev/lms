# -*- python -*-
# ex: set filetype=python:

from buildbot.plugins import *

c = BuildmasterConfig = dict()
repository_url = 'git://github.com/mesenev/lms.git'

c['workers'] = [worker.Worker("lms-ci-system", "pass")]
c['protocols'] = {'pb': {'port': 9989}}
c['builders'] = [
    util.BuilderConfig(name="lmsci", workernames=["lms-ci-system"], factory=factory),
]
c['change_source'] = [
    changes.GitPoller(repository_url, workdir='workdir', branches=True, pollInterval=40),
]
c['schedulers'] = [
    schedulers.AnyBranchScheduler(name="frontend", treeStableTimer=None, builderNames=["lms-ci-system"]),
]

factory = util.BuildFactory()
factory.addStep(steps.Git(repourl=repository_url, mode='incremental'))
factory.addStep(steps.ShellCommand(command=['cp', '../../scripts', 'scripts']))
factory.addStep(steps.ShellCommand(command=['cp', '../../.env', 'env.py']))
factory.addStep(steps.ShellCommand(command=['cp', '../../main.py', 'main.py']))
factory.addStep(steps.ShellCommand(command=['python', 'main.py'], ))

c['title'] = "lms building system"
c['titleURL'] = "mesenev/lms"

c['buildbotURL'] = "http://localhost:8010/"
c['www'] = dict(port=8010, plugins=dict(waterfall_view={}, console_view={}, grid_view={}))
c['db'] = {'db_url': "sqlite:///state.sqlite", }
