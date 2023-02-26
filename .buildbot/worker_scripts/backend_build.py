import subprocess


def build_composition():
    def build_message(code):
        if code:
            return 'composition fails to build. Aborting.'
        return 'composition build successful.'

    print('building docker composition')
    exec_code = subprocess.run(
        [
            "docker", "compose",
            "-f",
            ".docker/docker-compose.prod.yml",
            "build"
        ]).returncode
    return exec_code, build_message(exec_code)
