import argparse
import sys

from sawtooth_sdk.processor.core import TransactionProcessor
from sawtooth_sdk.processor.log import init_console_logging

from thutech_tp.handler import ThutechHandler


def parse_args(args):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
        '-C', '--connect',
        default='tcp://validator:4004',
        help='Endpoint for the validator connection')

    parser.add_argument(
        '-v', '--verbose',
        action='count',
        default=0,
        help='Increase output sent to stderr')

    return parser.parse_args(args)


def main(args=None):
    print("in main.py")
    if args is None:
        args = sys.argv[1:]
    opts = parse_args(args)
    processor = None
    try:
        print("in try")
        #init_console_logging(verbose_level=opts.verbose)

        processor = TransactionProcessor(url=opts.connect)
        print("processor")
        handler = ThutechHandler()
        print("handler object")
        processor.add_handler(handler)
        print("added handler to processor..")
        processor.start()
        print("processor started")
    except KeyboardInterrupt:
        print("keyboard interrupted..")
        pass
    except Exception as err:  # pylint: disable=broad-except
        print("Error: {}".format(err))
    finally:
        print("in final exception")
        if processor is not None:
            print("processor stopped")
            processor.stop()