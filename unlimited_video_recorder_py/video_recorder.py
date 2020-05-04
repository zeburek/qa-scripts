import subprocess
import threading

import time

from utils.logger import logger


def run_video_record(exe, event_for_wait):
    logger.info(exe)
    p = subprocess.Popen(
        exe.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    event_for_wait.wait()
    p.kill()
    event_for_wait.clear()


def copy_and_remove_record(file_name, path):
    p = subprocess.Popen(
        ("adb pull /sdcard/%s %s/%s" % (file_name, path, file_name)).split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    p.wait()
    p2 = subprocess.Popen(
        ("adb shell rm /sdcard/%s" % file_name).split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    p2.wait()
    logger.info("{}".format(time.time()))


def main():
    path = input("Path: ")
    while True:
        tmp_str = "%d.mp4" % time.time()
        video_string = "adb shell screenrecord /sdcard/%s" % tmp_str

        e1 = threading.Event()
        t1 = threading.Thread(target=run_video_record, args=(video_string, e1))
        t1.start()

        sec = 0
        while sec <= 60:
            time.sleep(1)
            sec += 1

        e1.set()

        t2 = threading.Thread(target=copy_and_remove_record(tmp_str, path))
        t2.start()


if __name__ == '__main__':
    main()
