import os
import sys
import worker_scripts as ws

sys.path.append('../')


sys.dont_write_bytecode = True


def chdir(directory):
    return lambda: [0, '', os.chdir(directory)][:2]


steps = [
        chdir('frontend'),
        ws.build_frontend,
        chdir('..'),
        ws.build_backend,
        ws.test_backend,
        ws.deploy_backend,
]


if __name__ == '__main__':
    ws.run(steps)
