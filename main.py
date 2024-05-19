import argparse

from app.database.sqlite import initialize_relation
from app.service import run, query, update_product_color


def cli():
    parser = argparse.ArgumentParser(description="Fruit Shop Sync CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("initdb", help="Initialize relation database with mock data")
    subparsers.add_parser("sync", help="Synchronize Fruit shop API data and relation data into MongoDB")
    subparsers.add_parser("query", help="Execute MongoDB query")
    subparsers.add_parser("update", help="Update product color through ChatGPT")

    args = parser.parse_args()

    if args.command == "initdb":
        initialize_relation()
    elif args.command == "sync":
        run()
    elif args.command == "query":
        query()
    elif args.command == "update":
        update_product_color()
    else:
        parser.print_help()


if __name__ == '__main__':
    cli()
