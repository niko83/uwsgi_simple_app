import os
import sys
import traceback                ## other uwsgi signals you define
import datetime, time
import uwsgidecorators
import random
import uwsgi
import threading

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
LOGS_PATH = ROOT_PATH + '/tmp/logs/'
TOUCHFILES_PATH = ROOT_PATH + '/tmp/touchfiles/'

def _colored(text, color='reset'):
    COLORS = { 'reset' : "\x1b[0m", 'green':"\x1b[32;01m", 'red':"\x1b[31;01m", 'gray':"\x1b[90;01m", 'white':"\x1b[1;01m"}
    return ''.join([COLORS[color], text, COLORS['reset']])

@uwsgidecorators.cron(30, 3, -1, -1, -1)
def cron(num):
    print '%s Every night on 3:00 run this code (signum %d)' % (datetime.datetime.now().strftime('%H:%M:%S'), num)
    time.sleep(50)

@uwsgidecorators.timer(1)
@uwsgidecorators.thread
@uwsgidecorators.lock
def f_timer(num):
    print '%s Every 10 seconds run this code (signum %d)' % (datetime.datetime.now().strftime('%H:%M:%S'), num)
    time.sleep(5)

@uwsgidecorators.filemon(TOUCHFILES_PATH + 'touch_me')
def touch(num):
    print '%s Touch file %s (signum %d)' % (datetime.datetime.now().strftime('%H:%M:%S'), TOUCHFILES_PATH + 'touch_me', num)

@uwsgidecorators.filemon(TOUCHFILES_PATH + 'spooler')
def start_spool(num):
    print '%s add procces  to spool (signum %d)' % (datetime.datetime.now().strftime('%H:%M:%S'), num)
    spool_proc.spool()

@uwsgidecorators.spool
def spool_proc(num):
    log_file = LOGS_PATH + 'spool.log'
    unique_id = random.randint(100, 900)
    tab = random.randint(1, 20)

    f = open(log_file, "a")
    f.write('\n' + '+' * tab +'start: '+str(unique_id))
    f.close()

    time.sleep(60)

    f = open(log_file, "a")
    f.write('\n' + '+' * tab + 'end  : '+str(unique_id))
    f.close()

@uwsgidecorators.filemon(TOUCHFILES_PATH + 'stack', target='workers')
def thread_dump(signum):
    output = ["\n\n"]
    output.append('{:=^60s} {:s}'.format(' BEGIN THREAD DUMP ', datetime.datetime.now().strftime('%H:%M:%S')))

    thread_names = dict([(t.ident, t.name) for t in threading.enumerate()])
    for threadId, stack in sys._current_frames().items():
        output.append(_colored('{:s}ThreadID: {:d} ({:s})'.format(' '*4, threadId, thread_names.get(threadId, 'NO_NAME_AVAILABLE')), 'white'))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            output.append(_colored('{:s}File: "{:s}", line {:d}, in {:s}'.format(' '*8, filename, lineno, name), 'gray'))
            if line:
                output.append('{:s}{:s}'.format(' '*8, line.strip()))
    output.append('{:=^60s}'.format(' END THREAD DUMP '))
    print '\n'.join(output)

@uwsgidecorators.postfork
def a_running_thread_with_args():
    print 'postfork job is started'


#@uwsgidecorators.filemon('/var/www/touchfiles/f1')
#@uwsgidecorators.postfork
#@uwsgidecorators.thread
#@uwsgidecorators.lock
# def a_running_thread_with_args(who=''):
    # while True:
        # time.sleep(2)
        # print("Hello %s (from arged-thread)" % who)

