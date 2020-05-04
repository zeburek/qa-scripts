import logging

logger = logging.getLogger("qa-scripts")
logger.setLevel(logging.INFO)

sh = logging.StreamHandler()
fmt = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s][%(message)s]")
sh.setFormatter(fmt)
logger.addHandler(sh)
