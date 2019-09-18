#! /usr/bin/env python
import argparse
from .censys_bigquery_cli import *


def main():

    args = argparse.ArgumentParser()

    # Add support for custom queries
    args.add_argument('query',
                      type=str)
    args.add_argument(
        '--filename',
        type=str,
        default=None,
        help='Assign a user-friendly name to the output file. Do not include the extension.'
    )

    args.add_argument('--output',
                      default="screen",
                      type=str,
                      nargs='+',
                      choices=["screen", "json", "csv"])

    # Future work
    #group = args.add_mutually_exclusive_group()
    #group.add_argument('--weeks', type=int, default=None)
    #group.add_argument('--months', type=int, default=None)

    parsed_args = args.parse_args()

    c = CensysBigQuery(user_filename=parsed_args.filename)
    c.query_censys(
        parsed_args.query,
        output_type=parsed_args.output
    )


if __name__ == '__main__':
    main()
