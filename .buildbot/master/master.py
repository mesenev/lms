# -*- python -*-
# ex: set filetype=python:

from buildbot.plugins import *

c = BuildmasterConfig = dict()
c['buildbotNetUsageData'] = 'basic'
repository_url = 'git://github.com/mesenev/lms.git'

c['workers'] = [
    worker.Worker("lms-worker-main", "pass"),
    worker.Worker("lms-worker-pr", "pass"),
    worker.Worker("lms-worker-force", "pass")
]

main_factory = util.BuildFactory()
main_factory.addStep(steps.Git(repourl=repository_url, mode='incremental'))
main_factory.addStep(steps.ShellCommand(command=['cp', '../../../worker-main/buildscript.py', '../buildscript.py']))
main_factory.addStep(steps.ShellCommand(command=['cp', '~/settings.py', 'imcslms/settings.py']))
main_factory.addStep(steps.ShellCommand(command=['cp', '~/common.env', '.docker/conf/common.env']))
main_factory.addStep(steps.ShellCommand(command=['cp', '~/common.env', 'frontend/.env']))
main_factory.addStep(steps.ShellCommand(command=['python', '../buildscript.py']))

force_factory = util.BuildFactory()
force_factory.addStep(steps.Git(repourl=repository_url, mode='full'))
force_factory.addStep(steps.ShellCommand(command=['cp', '../../../worker-main/buildscript.py', '../buildscript.py']))
force_factory.addStep(steps.ShellCommand(command=['cp', '~/settings.py', 'imcslms/settings.py']))
force_factory.addStep(steps.ShellCommand(command=['cp', '~/common.env', '.docker/conf/common.env']))
force_factory.addStep(steps.ShellCommand(command=['cp', '~/common.env', 'frontend/.env']))
force_factory.addStep(steps.ShellCommand(command=['python', '../buildscript.py']))

pr_factory = util.BuildFactory()
pr_factory.addStep(steps.Git(repourl=repository_url, mode='full'))
pr_factory.addStep(steps.ShellCommand(command=['cp', '../../worker_scripts', 'worker_scripts']))
pr_factory.addStep(steps.ShellCommand(command=['cp', '../../.env', 'env.py']))
pr_factory.addStep(steps.ShellCommand(command=['cp', '../../main.py', 'main.py']))
pr_factory.addStep(steps.ShellCommand(command=['python', 'buildscript.py'], ))

c['builders'] = [
    util.BuilderConfig(name="lmsci", workernames=["lms-worker-main"], factory=main_factory),
    util.BuilderConfig(name="lmspr", workernames=["lms-worker-pr"], factory=pr_factory),
    util.BuilderConfig(name="lmsforce", workernames=["lms-worker-force"], factory=main_factory),
]

c['protocols'] = {'pb': {'port': 9989}}
c['change_source'] = [
    changes.GitPoller(repository_url, workdir='workdir', branches=['main'], pollInterval=40),
    # changes.GitHubPullrequestPoller(owner='mesenev', repo='lms', pollInterval=20, name='pr_poller'),
    changes.GitPoller(
        repository_url,
        workdir='lmsforce', branch='main',
        pollInterval=300)
]

# def pr_filter(changes):
#     if hasattr(changes, 'category') and changes['category'] == 'pull':
#         return True
#     return False


c['schedulers'] = [
    schedulers.SingleBranchScheduler(
        name="main",
        treeStableTimer=5 * 60,
        change_filter=util.ChangeFilter(branch='main'),
        builderNames=["lmsci"]),
    schedulers.SingleBranchScheduler(
        name="pr",
        treeStableTimer=60,
        change_filter=util.ChangeFilter(category='pull'),
        builderNames=["lmspr"]),
    schedulers.ForceScheduler(
        name="force",
        builderNames=["lmsforce"])
]

c['title'] = "lms ci system"
c['titleURL'] = "mesenev/lms"

c['buildbotURL'] = "http://localhost:8010/"
c['www'] = dict(port=8010, plugins=dict(waterfall_view={}, console_view={}, grid_view={}))
c['www']['plugins']['profiler'] = True
c['db'] = {'db_url': "sqlite:///state.sqlite", }
