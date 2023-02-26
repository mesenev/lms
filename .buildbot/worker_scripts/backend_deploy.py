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
            "docker", "compose",
            "-f",
            ".docker/docker-compose.prod.yml",
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
            "docker", "compose",
            "-f",
            ".docker/docker-compose.prod.yml",
            "up",
            "--detach",
        ]).returncode
    message = '\n'.join([message, build_message_deploy(exec_code)])
    if exec_code:
        return exec_code, message
    print('making a migration')
    exec_code = subprocess.run(
        [
            "docker", "compose",
            "-f",
            ".docker/docker-compose.prod.yml",
            "exec",
            "-T",
            "backend",
            "sh", "-c",
            "python manage.py migrate --noinput",
        ]).returncode
    message = '\n'.join([message, 'migrations failed.' if exec_code else 'migrations applied successfully'])
    if exec_code:
        return exec_code, message
    print('collecting static')
    if exec_code:
        return exec_code, message
    exec_code = subprocess.run(
        [
            "docker", "compose",
            "-f",
            ".docker/docker-compose.prod.yml",
            "exec",
            "-T",
            "backend",
            "sh", "-c",
            "python manage.py collectstatic -c --noinput",
        ]).returncode
    message = '\n'.join([message, 'collectstatic failed.' if exec_code else 'collectstatic succeed'])
    return exec_code, message
