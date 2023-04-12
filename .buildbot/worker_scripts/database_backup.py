import subprocess
from datetime import datetime


def backup_database():
    def build_message(code):
        if code:
            return 'Backup ended with an error. Aborting.'
        return 'Backup completed successfully.'

    print('Making backup for db')
    exec_code = subprocess.run(
        ['docker', 'run', '--rm', '--volumes-from', 'database',
         '-v', f'/home/buildbot/database-backups/{datetime.now().strftime("%Y-%m-%d")}:/backup',
         'alpine',
         'tar', 'cvf',
         f'/backup/{datetime.now().strftime("%H:%M:%S")}.tar', '/var/lib/postgresql/data'
         ]
        ).returncode
    return exec_code, build_message(exec_code)
