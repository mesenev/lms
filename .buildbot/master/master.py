# -*- python -*-
# ex: set filetype=python:

from buildbot.plugins import *

c = BuildmasterConfig = dict()
c['buildbotNetUsageData'] = 'basic'
repository_url = 'git://github.com/mesenev/lms.git'

c['workers'] = [
    worker.Worker("lms-worker-main", "pass"),
    worker.Worker("lms-worker-pr", "pass")
]

main_factory = util.BuildFactory()
main_factory.addStep(steps.Git(repourl=repository_url, mode='incremental'))
main_factory.addStep(steps.ShellCommand(command=['cp', '../../scripts', 'scripts']))
main_factory.addStep(steps.ShellCommand(command=['cp', '../../.env', 'env.py']))
main_factory.addStep(steps.ShellCommand(command=['cp', '../../main.py', 'main.py']))
main_factory.addStep(steps.ShellCommand(command=['python', 'main.py'], ))

pr_factory = util.BuildFactory()
main_factory.addStep(steps.Git(repourl=repository_url, mode='full'))
main_factory.addStep(steps.ShellCommand(command=['cp', '../../worker_scripts', 'worker_scripts']))
main_factory.addStep(steps.ShellCommand(command=['cp', '../../.env', 'env.py']))
main_factory.addStep(steps.ShellCommand(command=['cp', '../../main.py', 'main.py']))
main_factory.addStep(steps.ShellCommand(command=['python', 'main.py'], ))

c['builders'] = [
    util.BuilderConfig(name="lmsci", workernames=["lms-worker-main"], factory=main_factory),
    util.BuilderConfig(name="lmspr", workernames=["lms-worker-pr"], factory=pr_factory),
]

c['protocols'] = {'pb': {'port': 9989}}
c['change_source'] = [
    changes.GitPoller(repository_url, workdir='workdir', branches=['main'], pollInterval=40),
    changes.GitHubPullrequestPoller(owner='mesenev', repo='lms', pollInterval=20, name='pr_poller')
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
]

c['title'] = "lms ci system"
c['titleURL'] = "mesenev/lms"

c['buildbotURL'] = "http://localhost:8010/"
c['www'] = dict(port=8010, plugins=dict(waterfall_view={}, console_view={}, grid_view={}))
c['db'] = {'db_url': "sqlite:///state.sqlite", }
