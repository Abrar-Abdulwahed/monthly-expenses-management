from app.interfaces.cli import run_cli
from app.interfaces.gui import run_gui
from app.core.storage import JsonStorage, MongoStorage
from app.core.decorators import log_exceptions


def choose_storage():
    print("Choose storage:")
    print("1) JSON")
    print("2) MongoDB")
    choice = input("Choose (1/2): ").strip()
    if choice == "2":
        return MongoStorage()
    return JsonStorage()


@log_exceptions
def main():
    storage = choose_storage()
    print("=== Start Application ===")
    print("1) CLI Mode")
    print("2) GUI Mode")
    choice = input("Choose (1/2): ").strip()

    if choice == "2":
        run_gui(storage)
    else:
        run_cli(storage)


if __name__ == "__main__":
    main()
