import sys
import os
import site


def is_venv() -> bool:
    return sys.prefix != sys.base_prefix


def print_venv_info() -> None:
    print("Virtual Environment:", end=" ")
    if is_venv():
        venv_path: str | None = os.getenv("VIRTUAL_ENV")
        if venv_path:
            print(os.path.basename(venv_path))
        print(
            "Environment Path:",
            venv_path
        )
    else:
        print("None detected")


def print_site_info() -> None:
    if is_venv():
        print("Package installation path:")
        print(site.getsitepackages()[0])


if __name__ == "__main__":
    print("MATRIX STATUS:", end=" ")
    if is_venv():
        print("Welcome to the construct")
    print("Current Python:", sys.executable)
    print_venv_info()
    print("")

    if is_venv():
        print(
            "SUCCESS: You're in an isolated environment!",
            "Safe to install packages without affecting the global system.\n",
            sep="\n"
        )
    else:
        print(
            "WARNING: You're in the global environment!",
            "The machines can see everything you install.\n",
            "python -m venv matrix_env",
            "source matrix_env/bin/activate # On Unix",
            "matrix_env\\Scripts\\activate # On Windows\n",
            "Then run this program again.",
            sep="\n"
        )
    print_site_info()
