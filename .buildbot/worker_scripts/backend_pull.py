import os
import subprocess

import dotenv


def pull_composition():
    dotenv.load_dotenv('/home/buildbot/buildbot.env')

    def build_message_registry_login(code):
        if code:
            return 'Failed to login to the registry.'
        return 'Registry login has been succeeded.'

    def build_message_pull(code):
        if code:
            return 'Composition images failed to pull.'
        return 'Composition images pulled from registry succeed.'

    message = ""
    print("Login to docker registry")
    exec_code = subprocess.run(
        [
            "docker", "login", "-u",
            os.getenv('DOCKER_REGISTRY_LOGIN'),
            "-p", os.getenv("DOCKER_REGISTRY_PASSWORD"),
            os.getenv("DOCKER_REGISTRY_ADDR")
        ]).returncode
    message = build_message_registry_login(exec_code)

    print('Pull composition images to registry🐳')
    exec_code = subprocess.run(
        [
            "docker",
            "pull",
            "registry.mesenev.ru/lms/backend:latest"
        ]).returncode
    message = '\n'.join([message, build_message_pull(exec_code)])
    return exec_code, message
