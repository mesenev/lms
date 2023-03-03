import os
import sys

sys.path.append('../../../')
sys.dont_write_bytecode = True

import worker_scripts as ws


def chdir(directory):
    return lambda: [0, '', os.chdir(directory)][:2]


steps = [
    chdir('frontend'),
    ws.build_frontend,
    chdir('..'),
    ws.build_composition,
    ws.test_backend,
    ws.push_composition,
]

if __name__ == '__main__':
    ws.run(steps)
