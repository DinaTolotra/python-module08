from os import getenv


log_level_mapping: dict[str, int] = {
    "off": 0,
    "error": 1,
    "debug": 2
}


class Config:
    def __init__(self, mode: str, db_url: str,
                 api_key: str, log_level: int,
                 endpoint: str) -> None:
        self.mode = mode
        self.db_url = db_url
        self.api_key = api_key
        self.log_level = log_level
        self.endpoint = endpoint

    def print(self) -> None:
        print(f"         Mode: {self.mode}")
        print(f"     Database: {self.db_url.split(':')[0]}")
        print(f"      API Key: {'*' * len(self.api_key)}")
        print(f"    Log Level: {self.log_level}")
        print(f"Zion Endpoint: {self.endpoint}")

    def connect_to_database(self) -> None:
        db: str = self.db_url.split(':')[0]
        host: str = self.db_url.split('@')[1].split('/')[0]
        user: str = self.db_url.split(':')[1].removeprefix('//')
        db_name: str = self.db_url.split('@')[1].split('/')[1]
        db_data: dict[str, str] = {
            "Database": db,
            "Host": host,
            "User": user,
            "Database name": db_name
        }
        invalid_list: list[str] = []

        for key, value in db_data.items():
            if value != "":
                print("[OK]", end="")
            else:
                print("[KO]", end="")
                invalid_list.append(key)
            print(" - ", key, ": ", value)

        if len(invalid_list) == 0:
            print("Status: connected")
        else:
            raise ValueError(
                "Invalid data in database url for: " +
                ", ".join(invalid_list)
            )


def check_config() -> None:
    config_key: list[str] = [
        "MATRIX_MODE",
        "DATABASE_URL",
        "API_KEY",
        "LOG_LEVEL",
        "ZION_ENDPOINT"
    ]
    missing_config_key: list[str] = []
    for key in config_key:
        if getenv(key) is None:
            print("[KO]", end=" ")
            missing_config_key.append(key)
        else:
            print("[OK]", end=" ")
        print(f"{key}")
    if missing_config_key:
        raise RuntimeError(
            "Missing configuration keys: " +
            ", ".join(missing_config_key)
        )


def check_config_values(mode: str, log_level: str) -> None:
    if mode not in ["developement", "production"]:
        raise ValueError(f"Invalid 'MATRIX_MODE': '{mode}'. " +
                         "Must be 'developement' or 'production'.")
    if log_level not in ["off", "error", "debug"]:
        raise ValueError(f"Invalid 'LOG_LEVEL': '{log_level}'. " +
                         "Must be one of 'off', 'error', 'debug'.")


def load_config() -> Config | None:
    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv()
    except Exception as e:
        print(f"[Error] - {e}")
        return None

    try:
        check_config()
    except RuntimeError as e:
        print(f"[Error] - {e}")
        return None

    (mode, db_url, api_key, log_level, endpoint) = (
        getenv("MATRIX_MODE", "").lower(),
        getenv("DATABASE_URL", ""),
        getenv("API_KEY", ""),
        getenv("LOG_LEVEL", "").lower(),
        getenv("ZION_ENDPOINT", "")
    )
    
    try:
        check_config_values(mode, log_level)
    except ValueError as e:
        print(f"[Error] - {e}")
        return None

    return Config(
        mode, db_url, api_key,
        log_level_mapping.get(log_level, 0),
        endpoint
    )


def main() -> None:
    print("=== Accessing the Mainframe ===")
    print("\n[Log] - Loading configuration...")
    config = load_config()
    if config is None:
        print("[Log] - Configuration loading failed")
        print("[Log] - Aborted")
        return

    print()
    config.print()
    if config.log_level >= 2:
        print("[Log] - Configuration loaded successfully")

    if config.mode == "developement":
        if config.log_level >= 2:
            print("\n[Log] - Running in developement mode")
    else:
        if config.log_level >= 2:
            print("\n[Log] - Running in production mode")

    print()
    if config.log_level >= 2:
        print("\n[Log] - Connecting to the database...")
    try:
        config.connect_to_database()
        if config.log_level >= 2:
            print("[Log] - Connected to the database successfully")
    except ValueError as e:
        if config.log_level >= 1:
            print(f"[Error] - {e}")
        if config.mode == "developement":
            if config.log_level >= 2:
                print("[Log] - Aborted")
            return
        elif config.log_level >= 2:
            print("[Log] - Skipped")

    print()
    print("Running application...")


if __name__ == "__main__":
    main()
