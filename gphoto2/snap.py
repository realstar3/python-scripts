import os
import click
import sys
import signal
import time
from subprocess import Popen, PIPE

print("BEGIN")
global ca_pid
global p1
@click.command()
@click.option("--name", prompt="ENTER NAME", help="Your name")
@click.option("--position", prompt="ENTER POSITION", help="Your position")
def hello(name, position):
    click.echo('Hello, {}, {} !'.format(name, position))
    adding_keypress_in_logfile("name : {}\n".format(name))
    adding_keypress_in_logfile("position : {}\n".format(position))
    print("sit down and push the left pedal to start recording...")

    listOfStrings = ["a", "b", "c", "x", "h", "help"]
    pedal = ""
    s_flag = False
    while True:

        while True:
            pedal = str(raw_input())
            # pedal = str(input())

            if pedal in listOfStrings:
                break
            print("pedal is incorrect:{}".format(pedal))

        if pedal == "a":
            if not s_flag:
                s_flag = True
            else:
                s_flag = False

            adding_keypress_in_logfile("key : {}\n".format(pedal))
            capture_movie(s_flag)

        if pedal == "b":
            adding_keypress_in_logfile("key : {}\n".format(pedal))
            capture_image()
        if pedal == "c":
            disp_log()
        if pedal in ["h", "help"]:
            print("Help :")
            print("   a : start/stop recording")
            print("   b : take photo with countdown from 3 sec")
            print("   c : display log")
            print("   x : exit ")
        if pedal == "x":
            sys.exit("bye!")


def signal_handler(*args):
    print("received signal\n")
    signal_and_reinput()


signal.signal(signal.SIGINT, signal_handler)


def capture_movie(flag):
    global ca_pid
    global p1

    if flag:
        print("starting capture movie")
        p1 = Popen(["gphoto2 --capture-movie"], stdout=PIPE, stderr=PIPE,shell=True)
        global ca_pid
        ca_pid = p1.pid
        print("pid:", ca_pid)

        # output, err = p1.communicate()
        # if err is None:
        #     print(output)
        #     adding_keypress_in_logfile(output)
        #     print("success : capture movie.")
        # else:
        #     print(err)
        #     adding_keypress_in_logfile(err)
        #     print("fail : capture movie.")
    else:
        print(str(p1))
        if not p1 is None:
            try:
                kill_child()
            except OSError:
                # p1.kill()
                # outs, errs = p1.communicate()
                # print("outs:", outs)
                # print("errs:", errs)
                ca_pid = 0
                return
            print("stopped capturing movie")
        else:
            print("ca_pid is 0")

def kill_child():
    if ca_pid is None:
        pass
    else:
        os.kill(ca_pid, signal.SIGTERM)
        os.kill(ca_pid+1, signal.SIGTERM)

def capture_image():
    print("capture image later 3 seconds....")
    i = 1
    while i < 4:
        time.sleep(1)
        print(str(i) + ":second")
        i = i + 1
    print("starting capture image.")
    # p1 = Popen(["gphoto2", "--capture-image-and-download"], stdout=PIPE)
    p2 = Popen(["gphoto2 --capture-image"], stdout=PIPE, shell=True)
    output, err = p2.communicate()
    if err is None:
        print(output)
        adding_keypress_in_logfile(output)
        print("success : capture image.")
    else:
        print(err)
        adding_keypress_in_logfile(err)
        print("fail : capture image.")


def adding_keypress_in_logfile(keypress):
    with open('keypress_log.txt', 'a') as the_file:
        the_file.write(keypress)


def disp_log():

    with open('keypress_log.txt') as the_file:
        read_data = the_file.read()
        print(read_data)


def signal_and_reinput():
    listOfStrings = ["a", "b", "c", "x", "h", "help"]
    pedal = ""
    s_flag = False
    while True:

        while True:
            pedal = str(raw_input())
            # pedal = str(input())

            if pedal in listOfStrings:
                break
            print("pedal is incorrect:{}".format(pedal))

        if pedal == "a":
            if not s_flag:
                s_flag = True
            else:
                s_flag = False

            adding_keypress_in_logfile("key : {}\n".format(pedal))
            capture_movie(s_flag)

        if pedal == "b":
            adding_keypress_in_logfile("key : {}\n".format(pedal))
            capture_image()
        if pedal == "c":
            disp_log()
        if pedal in ["h", "help"]:
            print("Help :")
            print("   a : start/stop recording")
            print("   b : take photo with countdown from 3 sec")
            print("   c : display log")
            print("   x : exit ")
        if pedal == "x":
            sys.exit("bye!")

if __name__ == '__main__':
    p1 = None
    s_flag = True
    ca_pid = 0
    fw = open('keypress_log.txt', 'w')
    fw.write('')
    hello()

