import subprocess

import dotenv


def reload_backend():
    dotenv.load_dotenv('/home/buildbot/buildbot.env')

    def build_message_reload(code):
        if code:
            return 'Docker compose with new image reload failed.'
        return 'Docker compose with new image reload is succeeded.'

    exec_code = subprocess.run(
        [
            "docker", "compose", "-f",
            ".docker/docker-compose.prod.yml",
            "up", "--detach"
        ]).returncode
    message = build_message_reload(exec_code)
    if exec_code:
        return exec_code, message
    print('making a migration')
    exec_code = subprocess.run([
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
