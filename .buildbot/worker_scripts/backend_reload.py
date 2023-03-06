import subprocess

import dotenv


def reload_backend():
    dotenv.load_dotenv('home/buildbot/buildbot.env')

    def build_message_reload(code):
        if code:
            return 'Docker compose with new image reload failed.'
        return 'Docker compose with new image reload is succeeded.'

    print('Pull composition images to registry🐳')
    exec_code = subprocess.run(
        [
            "docker", "compose", "-f",
            ".docker/docker-compose.prod.yml",
            "up", "backend", "beat", "--no-debs"
        ]).returncode
    message = build_message_reload(exec_code)
    return exec_code, message
