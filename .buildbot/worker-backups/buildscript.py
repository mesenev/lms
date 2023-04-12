import sys

sys.path.append('../../../')
sys.dont_write_bytecode = True

import worker_scripts as ws

steps = [
    ws.backup_database,
]

if __name__ == '__main__':
    ws.run(steps)
