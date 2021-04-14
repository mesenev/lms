# -*- python -*-
# ex: set filetype=python:

from buildbot.plugins import *

c = BuildmasterConfig = dict()
c['buildbotNetUsageData'] = 'basic'
repository_url = 'git://github.com/mesenev/lms.git'

c['workers'] = [worker.Worker("lms-ci-worker", "pass")]

factory = util.BuildFactory()
factory.addStep(steps.Git(repourl=repository_url, mode='incremental'))
factory.addStep(steps.ShellCommand(command=['cp', '../../scripts', 'scripts']))
factory.addStep(steps.ShellCommand(command=['cp', '../../.env', 'env.py']))
factory.addStep(steps.ShellCommand(command=['cp', '../../main.py', 'main.py']))
factory.addStep(steps.ShellCommand(command=['python', 'main.py'], ))

c['builders'] = [
    util.BuilderConfig(name="lmsci", workernames=["lms-ci-worker"], factory=factory),
]

c['protocols'] = {'pb': {'port': 9989}}
c['change_source'] = [
    changes.GitPoller(repository_url, workdir='workdir', branches=True, pollInterval=40),
]
c['schedulers'] = [
    schedulers.SingleBranchScheduler(
        name="frontend",
        treeStableTimer=5*60,
        change_filter=util.ChangeFilter(branch='main'),
        builderNames=["lmsci"]),
]

c['title'] = "lms ci system"
c['titleURL'] = "mesenev/lms"

c['buildbotURL'] = "http://localhost:8010/"
c['www'] = dict(port=8010, plugins=dict(waterfall_view={}, console_view={}, grid_view={}))
c['db'] = {'db_url': "sqlite:///state.sqlite", }
