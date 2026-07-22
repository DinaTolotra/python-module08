from importlib.util import find_spec
from importlib.metadata import metadata, PackageMetadata
from importlib import import_module
from sys import prefix, base_prefix
from sys import stderr


def check_env() -> None:
    pkg_list: list[str] = [
        "numpy", "pandas", "matplotlib"]
    pkg_missing: list[str] = []
    pkg_metadata: PackageMetadata

    if prefix == base_prefix:
        raise RuntimeError(
            "virtual environment not found")

    for pkg in pkg_list:
        if find_spec(pkg):
            pkg_metadata = metadata(pkg)
            print(f"[OK] {pkg} - "
                  f"({pkg_metadata['Version']}):",
                  pkg_metadata['Summary'])
        else:
            print(f"[KO] {pkg}")
            pkg_missing.append(pkg)

    if pkg_missing:
        raise RuntimeError(
            f"missing packages: {', '.join(pkg_missing)}")


def print_usage() -> None:
    print("Usage:")
    print("\n$ # pip")
    print("$ python -m venv venv")
    print(" or \n$ /opt/pyenv/versions/3.13.*/bin/python -m venv venv")
    print("$ source venv/bin/activate{.sh|.fish}")
    print("$ pip install -r requirements.txt")
    print("$ python loading.py")
    print("$ # Tool used: 'pip', 'venv', ./requirements.txt")
    print("$ # To support a full project, 'pip' are not enough")
    print("\n$ # poetry")
    print("$ poetry install")
    print("$ poetry env use python3.13", end="")
    print(" # or /opt/pyenv/versions/3.13.*/bin/python")
    print("$ poetry run python loading.py")
    print("$ # Tool used: 'poetry', ./pyproject.toml")
    print("$ # 'poetry' can manage a project alone")


def main() -> None:
    pd = np = plt = None
    try:
        check_env()
        pd = import_module("pandas")
        np = import_module("numpy")
        plt = import_module("matplotlib.pyplot")
        print("[Log] Dependencies satisfied")
    except RuntimeError as e:
        print(f"[Error] {e}\n", file=stderr)
        print_usage()
        return

    day_count = 7
    rng = np.random.default_rng()
    x = np.arange(1, day_count + 1)
    print("[Log] Generating random data: income/outcome")
    y_income = x * rng.random(day_count)
    y_outcome = x * rng.random(day_count)

    print("[Log] Manipulating data")
    daily_income = pd.DataFrame({
        "Day": x,
        "Value": y_income
    })
    daily_outcome = pd.DataFrame({
        "Day": x,
        "Value": y_outcome
    })
    saving = pd.DataFrame({
        "Day": x,
        "Value": np.cumsum(y_income - y_outcome)
    })

    print("[Log] Setting up plot")
    plt.plot(daily_income["Day"], daily_income["Value"],
             label="Income", color="green")
    plt.plot(daily_outcome["Day"], daily_outcome["Value"],
             label="Outcome", color="red")
    plt.plot(saving["Day"], saving["Value"],
             label="Saving", color="blue")
    plt.plot(np.array([0] * day_count), color="black")
    plt.legend()
    print("[Log] Saving figure")
    plt.savefig("output.png")
    plt.close()
    print("[Log] Done!")


if __name__ == "__main__":
    main()
