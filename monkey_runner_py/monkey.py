import sys
import time
import re

from utils import run_process, mkdir_p
from utils.logger import logger


def get_selected_device():
    devices = []
    for line in run_process("adb devices".split()):
        line = line.replace("\r", "").replace("\n", "")
        if "List" not in line:
            if line:
                devices.append(re.sub("\t\S*", "", line))
    logger.info("Available device IDs:")
    i = 0
    for device in devices:
        logger.info("%d\t\t%s" % (i, device))
        i += 1
    dev_id = int(input("Input device ID: "))
    if devices[dev_id]:
        return devices[dev_id]
    else:
        return devices[0]


def main():
    mkdir_p("results")
    ts = time.time()
    mkdir_p("results/%d" % ts)
    mkdir_p("results/%d/videos" % ts)
    print("./results/%d/videos" % ts)
    filename = "results/%d/result_%s.log" % (ts, ts)
    with open(filename, "w+") as file:
        file.write("# Created at %s" % ts)

    device = get_selected_device()

    package = int(input("Please provide package ID: "))
    how_much = int(input("Inter number of steps (1000000): "))
    monkey_command = (
        'adb -s {} shell monkey -p {} -v -v -v '
        '--ignore-crashes --ignore-timeouts '
        '--ignore-security-exceptions --monitor-native-crashes '
        '--pct-syskeys 0 {}'.format(device, package, how_much)
    )

    percent = float(how_much) / 100
    already_done = 0
    injection_failed = 0
    freeze = 0
    crash = 0
    anr = 0
    monkey_log = ""

    for line in run_process(monkey_command.split()):
        monkey_log += line
        if ":Sending" in line:
            already_done += 1
        if "Injection Failed" in line:
            injection_failed += 1
        if "CRASH" in line:
            crash += 1
        if "ANR" in line:
            anr += 1
        if injection_failed == 20:
            run_process("adb -s %s shell am force-stop %s" % (device, package))
            freeze += 1
            injection_failed = 0
            logger.info('[INFO]: Freezed, restarting application')
        if line.startswith("// "):
            if not line.startswith("//   - NOT USING"):
                logger.info("\n[INFO]: %s" % line)
                with open(filename, "a") as file:
                    file.write("%s" % line)
            continue
        result_percent = already_done / percent
        print('\rProcess: %.2f%%' % result_percent)
        sys.stdout.flush()

    print('\rProcess: %.2f%%' % 100)
    sys.stdout.flush()
    print('[INFO]: Monkey finished on %s iteration' % already_done)
    print('[INFO]: Freezed %d times' % freeze)
    print('[INFO]: Crashed %d times' % crash)
    print('[INFO]: ANR was %d times' % anr)
    with open(filename, "a") as file:
        file.write("%s" % monkey_log)


if __name__ == "__main__":
    main()
