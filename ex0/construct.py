import sys
import os
import site


def is_virtual_env() -> bool:
    return sys.prefix != sys.base_prefix


def print_venv_info() -> None:
    print("Virtual Environment: ", end="")
    venv_path: str | None
    if is_virtual_env():
        venv_path = os.getenv("VIRTUAL_ENV")
        if venv_path is not None:
            print(os.path.basename(venv_path))
        print("Environment Path:", venv_path)
    else:
        print("None detected")


def print_site_info() -> None:
    if is_virtual_env():
        print("Package installation path:")
        print(site.getsitepackages()[0])


def main() -> None:
    print("MATRIX STATUS:", end=" ")
    if is_virtual_env():
        print("Welcome to the construct")
    print("Current Python:", sys.executable)
    print_venv_info()
    print("")

    if is_virtual_env():
        print("SUCCESS: You're in an isolated environment!\n",
              "Safe to install packages without",
              "affecting the global system.\n")
    else:
        print("WARNING: You're in the global environment!\n",
              "The machines can see everything you install.\n\n",
              "To create an isolated environment, ",
              "run the following commands:\n",
              "$ python -m venv matrix_env\n",
              "$ source matrix_env/bin/activate # On Unix\n",
              "$ matrix_env\\Scripts\\activate # On Windows\n\n",
              "Then run this program again.")
    print_site_info()


if __name__ == "__main__":
    main()
