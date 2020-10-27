"""Generic Utils"""
import logging
import argparse
from typing import List
from pathlib import Path
from sobers import config
from sobers.plugins import Transformation

logger = logging.getLogger(__name__)


def read_and_transform_csv(path_to_file: Path, processor: Transformation) -> List[str]:
    """Read the file and apply transformations

    :param path_to_file: source csv file path
    :param processor: transformations defined for a given row
    :return: transformed rows
    """
    with open(path_to_file, 'r') as reader:
        rows = reader.readlines()
        logger.debug('Column names of CSV: %s ' % rows[0])

        processed_lines = []

        # skip the header and process the actual data
        for row in rows[1:]:
            cleaned = processor(row)
            processed_lines.append(cleaned)

        return processed_lines


def write_to_csv(path_to_dest: Path, content: List[str], header: List[str] = config.OUT_ATTRS):
    """Write to destination file

    :param path_to_dest: destination file
    :param content: contents to write
    :param header: header information
    :return: None
    """
    header = ",".join(header)
    full_content = header + '\n' + '\n'.join(content)

    with open(path_to_dest, 'w') as writer:
        writer.write(full_content)
    logger.info("Outputted to %s" % path_to_dest)


def get_args():
    """Parse command line arguments

    :return: `ArgumentParser`
    """
    # Create the parser
    parser = argparse.ArgumentParser(description='SOBERS Assignment')

    # Add the arguments

    parser.add_argument('--source-path',
                        type=str,
                        required=True,
                        help='Path to CSV File')

    parser.add_argument("--transformation",
                        type=str,
                        required=True,
                        help="Bank Name (defines transformations)")

    parser.add_argument("--out-path",
                        type=str,
                        default=None,
                        required=False,
                        help='Outputhdirectory to save csv')

    parser.add_argument('--verbose',
                        action='store_true',
                        help='set logging to DEBUG')

    return parser.parse_args()
