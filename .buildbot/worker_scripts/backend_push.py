import subprocess


def push_composition():
    def build_message(code):
        if code:
            return 'Composition images failed to push.'
        return 'Composition images push to registry succeed.'

    print('Push composition images to registry')
    exec_code = subprocess.run(
        [
            "docker", "compose", "-f",
            ".docker/docker-compose.prod.yml",
            "push"
        ]).returncode
    return exec_code, build_message(exec_code)
