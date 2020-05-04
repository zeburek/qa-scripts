from utils import run_process
from utils.logger import logger


def open_urls():
    with open("urls.txt", 'r') as file:
        for link in file:
            for line in run_process(
                "adb shell am start -a android.intent.action.VIEW "
                "-c android.intent.category.BROWSABLE -d \"{}\"".format(link)
            ):
                if line:
                    logger.info(line)
            input("Next...")


def main():
    logger.info("Will open given urls from urls.txt")
    open_urls()


if __name__ == '__main__':
    main()
