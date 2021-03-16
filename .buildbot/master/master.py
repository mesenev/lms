# -*- python -*-
# ex: set filetype=python:

from buildbot.plugins import *

c = BuildmasterConfig = {}
repository_url = 'git://github.com/mesenev/lms.git'

# WORKERS

# The 'workers' list defines the set of recognized workers. Each element is
# a Worker object, specifying a unique worker name and password.  The same
# worker name and password must be configured on the worker.
c['workers'] = [worker.Worker("frontend-build-worker", "pass")]

c['protocols'] = {'pb': {'port': 9989}}

c['change_source'] = []
c['change_source'].append(
    changes.GitPoller(
        repository_url,
        workdir='workdir', branches=True,
        pollInterval=40
    )
)

c['schedulers'] = []
c['schedulers'].append(schedulers.AnyBranchScheduler(
    name="frontend",
    treeStableTimer=None,
    builderNames=["buildfrontend"]
))

factory = util.BuildFactory()
factory.addStep(steps.Git(repourl=repository_url, mode='incremental'))

factory.addStep(steps.ShellCommand(
    command=['cp', '../../notification.py', 'notification.py']
))
factory.addStep(steps.ShellCommand(
    command=['cp', '../../.env', 'env.py']
))
factory.addStep(steps.ShellCommand(
    command=['cd', 'frontend']
))
factory.addStep(steps.ShellCommand(
    command=['npm', 'install']
))
factory.addStep(steps.ShellCommand(
    command=['cd', '..']
))
factory.addStep(steps.ShellCommand(
    command=['python', 'notification.py'],
))

c['builders'] = []
c['builders'].append(
    util.BuilderConfig(
        name="buildfrontend",
        workernames=["frontend-build-worker"],
        factory=factory)
)

c['title'] = "lms building system"
c['titleURL'] = "mesenev/lms"

c['buildbotURL'] = "http://localhost:8010/"
c['www'] = dict(
    port=8010, plugins=dict(
        waterfall_view={}, console_view={}, grid_view={})
)
c['db'] = {'db_url': "sqlite:///state.sqlite", }
