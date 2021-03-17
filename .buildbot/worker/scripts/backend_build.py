import subprocess


def build_message(code):
    if code:
        return 'composition fails to build. Aborting.'
    return 'composition build successful.'


def build_backend():
    exec_code = subprocess.run(
        [
            "docker-compose",
            "-f",
            ".docker/docker-compose.dev.yml",
            "build"
        ]).returncode
    return exec_code, build_message(exec_code)
