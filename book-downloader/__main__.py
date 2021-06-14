import argparse
import logging
import os

from .main import download

parser = argparse.ArgumentParser(
    description="Download a book from Internet Archive",
)

parser.add_argument(
    "-e",
    "--email",
    nargs=1,
    type=str,
    help="Email to log in",
)

parser.add_argument(
    "-p",
    "--password",
    nargs=1,
    type=str,
    help="Password to log in",
)

parser.add_argument(
    "url",
    type=str,
    nargs="+",
    help="Urls of books",
)

parser.add_argument(
    "-o",
    "--output",
    nargs=1,
    type=str,
    help="Output folder",
)

parser.add_argument(
    "-v",
    "--verbose",
    action="store_const",
    dest="loglevel",
    const=logging.INFO,
    help="Increase output verbosity",
)

parser.add_argument(
    "-vv",
    "--debug",
    action="store_const",
    dest="loglevel",
    const=logging.DEBUG,
    default=logging.WARNING,
    help="Increase output verbosity for debugging",
)

parser.add_argument(
    "-s",
    "--show-browser",
    action="store_true",
    help="Show browser window",
)

args = parser.parse_args()
logging.basicConfig(level=args.loglevel)

try:
    os.environ.pop("MOZ_HEADLESS")
except:
    pass

if not args.show_browser:
    os.environ["MOZ_HEADLESS"] = "1"

download(args.url, args.output[0], args.email[0], args.password[0])