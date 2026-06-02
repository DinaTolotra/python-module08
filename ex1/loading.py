from importlib.util import find_spec
from importlib.metadata import version
from sys import prefix, base_prefix


def check_env() -> None:
    pkg_list: list[str] = [
        "numpy", "pandas", "matplotlib"]
    if prefix == base_prefix:
        raise RuntimeError(
            "virtual environment not found")
    for pkg in pkg_list:
        if find_spec(pkg):
            print(f"[OK] {pkg} - "
                  f"({version(pkg)})")
        else:
            print(f"[KO] {pkg}")
            raise RuntimeError(
                f"package '{pkg}' not found")


def print_usage() -> None:
    print("Usage:")
    print("\n$ # pip")
    print("$ python -m venv venv")
    print("$ source venv/bin/activate{.sh|.fish}")
    print("$ pip install -r requirements.txt")
    print("$ python loading.py")
    print("\n$ # poetry")
    print("$ poetry install")
    print("$ poetry env use python3.13")
    print("$ poetry run python3.13 loading.py")


if __name__ == "__main__":
    try:
        print("[LOG] Checking deps...")
        check_env()
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
    except RuntimeError as e:
        print("Error:", e)
        print_usage()
    else:
        count = 100
        rng = np.random.default_rng()
        num = np.arange(count)
        dates = np.arange(
            '2026-06-01',
            '2026-06-10',
            dtype=np.datetime64)
        print("\n[LOG] Generating data...")
        score = rng.uniform(0, 100, (len(dates), count))
        score = np.round(score, 2)
        print("[LOG] Arranging data...")
        raw_df = pd.DataFrame(
            score,
            columns=num,
            index=dates)
        avg_df = raw_df.mean()
        print("=== DataFrame ===")
        print(raw_df.info(verbose=False))
        print("=================")
        print("[LOG] Generating visualization...")
        avg_df.plot(
            title="player score average",
            xlabel="num",
            ylabel="avg"
        )
        plt.savefig("player_score.png")
        print("[LOG] Figure saved to: player_score.png")
