import logging
from pathlib import Path

from sobers import constants
from sobers.config import LOGGING_FORMAT
from sobers.utils import get_args, write_to_csv, read_and_transform_csv

logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    args = get_args()

    # Set log level to DEBUG if verbose is set
    if args.verbose:
        level = logging.getLevelName('DEBUG')
        logger.setLevel(level)

    logger.debug("Parsed values: %s" % str(args))

    # Set the output path to export files
    out_path = Path(__file__).resolve().parent if not args.out_path else Path(args.out_path)
    logger.debug('Output directory: %s' % out_path)

    # check if bank name is listed in configs (has transformation defined)
    if args.transformation not in constants.streams:
        logger.error('Bank name of %s is not in available list of %s' % (args.transformation, constants.streams.keys()))
        raise ValueError(f"Ensure bank name is defined. Available names: {constants.streams.keys()}")

    processor = constants.streams.get(args.transformation)
    logger.debug("Processor details: %s" % processor)

    # read and transform contents from source csv
    source = Path(args.source_path)
    contents = read_and_transform_csv(args.source_path, processor)

    # Write transformed output to dest
    out_file_path = out_path / f"{args.transformation}.csv"
    write_to_csv(out_file_path, contents)

    logger.info('Finished successfully')


if __name__ == '__main__':
    main()
