import os
import sys
import traceback                ## other uwsgi signals you define
import datetime, time
import uwsgidecorators
import random

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

@uwsgidecorators.cron(30, 3, -1, -1, -1)
def cron(num):
    print '%s Every night on 3:00 run this code (signum %d)' % (datetime.datetime.now().strftime('%H:%M:%S'), num)
    time.sleep(50)

@uwsgidecorators.timer(30)
@uwsgidecorators.thread
def f_timer(num):
    print '%s Every 30 seconds run this code (signum %d)' % (datetime.datetime.now().strftime('%H:%M:%S'), num)
    time.sleep(25)

@uwsgidecorators.filemon(ROOT_PATH + '/tmp/touchfiles/touch_me')
def touch(num):
    print '%s Touch file %s (signum %d)' % (datetime.datetime.now().strftime('%H:%M:%S'), ROOT_PATH + '/tmp/touchfiles/touch_me', num)
    spool_proc.spool()

@uwsgidecorators.filemon(ROOT_PATH + '/tmp/touchfiles/start_spool_proc')
def start_spool(num):
    print '%s add procces  to spool (signum %d)' % (datetime.datetime.now().strftime('%H:%M:%S'), num)
    spool_proc.spool()

@uwsgidecorators.spool
def spool_proc(num):
    log_file = ROOT_PATH + '/tmp/logs/spool.log'
    f = open(log_file, "a")
    numberS = random.randint(100, 900)
    tab = random.randint(1, 20)
    f.write('\n' + '+' * tab +'start: '+str(numberS))
    f.close()
    time.sleep(60)
    f = open(log_file, "a")
    f.write('\n' + '+' * tab + 'end  : '+str(numberS))
    f.close()

# @uwsgidecorators.spool
# def f6(num):
    # FILE = '/var/www/env/mws/f1'
    # import time, random
    # f = open(FILE, "a")
    # numberS = random.randint(100, 900)
    # tab = random.randint(1, 20)
    # f.write('\n' + '+' * tab +'2ta: '+str(numberS))
    # f.close()


    # for a in xrange(120000000):
        # pass

    # f = open(FILE, "a")
    # f.write('\n' + '+' * tab + '2nd: '+str(numberS))
    # f.close()
# @uwsgidecorators.filemon('/var/www/touchfiles/f2')
# def f5(num):
    # f6.spool()

# @uwsgidecorators.timer(1)
# @uwsgidecorators.thread
# def f4(num):
    # import time
    # print 'start'
    # time.sleep(50)
    # print 'finish'

#@uwsgidecorators.filemon('/var/www/touchfiles/f1')
#@uwsgidecorators.postfork
#@uwsgidecorators.thread
#@uwsgidecorators.lock
# def a_running_thread_with_args(who=''):
    # while True:
        # time.sleep(2)
        # print("Hello %s (from arged-thread)" % who)

# import uwsgi
# uwsgidecorators.filemon('/var/www/touchfiles/reload')(uwsgi.reload)


stack_dump_file = ROOT_PATH + '/tmp/touchfiles/stack'  ## given as an example; put this somewhere better than /tmp
uwsgi_signal_number = uwsgidecorators.get_free_signal()
import uwsgi
import threading

#@uwsgidecorators.filemon('/var/www/uwsgi_simple_app/src/tmp/touchfiles/stack')
def thread_dump(dummy_signum):
    output = []
    output.append("\n\n### BEGIN THREAD DUMP")

    thread_names = dict([(t.ident, t.name) for t in threading.enumerate()])
    for threadId, stack in sys._current_frames().items():
        output.append("# ThreadID: %s (%s)" % (threadId, thread_names.get(threadId, 'NO_NAME_AVAILABLE')))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            output.append('File: "%s", line %d, in %s' % (filename, lineno, name))
            if line:
                output.append(" %s" % (line.strip()))
    output.append("### END THREAD DUMP")
    print '\n'.join(output)

uwsgi.register_signal(uwsgi_signal_number, 'workers', thread_dump)
uwsgi.add_file_monitor(uwsgi_signal_number, stack_dump_file)

