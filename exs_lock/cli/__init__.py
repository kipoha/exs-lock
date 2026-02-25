import argparse

from exs_lock.cli.lock import lock_cmd
from exs_lock.cli.version import version_cmd


def main():
    parser = argparse.ArgumentParser(
        prog="exs-lock",
        description="EXS Lock CLI"
    )

    parser.add_argument(
        "command",
        nargs="?",
        choices=["version"],
        help="Show version"
    )

    parser.add_argument(
        "--dev",
        action="store_true",
        help="Run in development mode"
    )

    args = parser.parse_args()

    if args.command == "version":
        version_cmd(args)
    else:
        lock_cmd(args)


if __name__ == "__main__":
    main()
