import subprocess


def build_message_database(code):
    if code:
        return 'Database deploy failed.'
    return 'Database ok.'


def build_message_deploy(code):
    if code:
        return 'Composition deploy failed'
    return 'Composition deployed'


def deploy_backend():
    print('deploying database')
    exec_code = subprocess.run(
        [
            "docker-compose",
            "-f",
            ".docker/docker-compose.yml",
            "up",
            "--detach",
            "database"
        ]).returncode
    message = build_message_database(exec_code)
    if exec_code:
        return exec_code, message
    print('deploying composition')
    exec_code = subprocess.run(
        [
            "docker-compose",
            "-f",
            ".docker/docker-compose.yml",
            "up",
            "--detach",
        ]).returncode
    return exec_code, '\n'.join([message, build_message_deploy(exec_code)])
