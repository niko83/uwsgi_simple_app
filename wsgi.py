import os
import sys
import traceback                                            ## other uwsgi signals you define

import uwsgidecorators


def application(environ, start_response):
    status = '200 OK'
    output = 'Hello World!'
    response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]


@uwsgidecorators.cron(-1,-1,-1,-1,-1)
def f2(num):
    print str(num)+'__cron'

@uwsgidecorators.spool
def f3(num):
    FILE = '/var/www/env/mws/f1'
    import time, random
    f = open(FILE, "a")
    numberS = random.randint(100, 900)
    tab = random.randint(1, 20)
    f.write('\n' + '+' * tab +'sta: '+str(numberS))
    f.close()

    for a in xrange(120000000):
        pass

    f = open(FILE, "a")
    f.write('\n' + '+' * tab + 'end: '+str(numberS))
    f.close()

@uwsgidecorators.filemon('/var/www/touchfiles/f1')
def f4(num):
    f3.spool()

@uwsgidecorators.spool
def f6(num):
    FILE = '/var/www/env/mws/f1'
    import time, random
    f = open(FILE, "a")
    numberS = random.randint(100, 900)
    tab = random.randint(1, 20)
    f.write('\n' + '+' * tab +'2ta: '+str(numberS))
    f.close()


    for a in xrange(120000000):
        pass

    f = open(FILE, "a")
    f.write('\n' + '+' * tab + '2nd: '+str(numberS))
    f.close()
@uwsgidecorators.filemon('/var/www/touchfiles/f2')
def f5(num):
    f6.spool()

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


stack_dump_file = '/var/www/touchfiles/stack'  ## given as an example; put this somewhere better than /tmp
uwsgi_signal_number = 17                    ## nothing magic about this number; just can't conflict with
try:
    import uwsgi
    import threading

    if not os.path.exists(stack_dump_file):
        open(stack_dump_file, 'w')

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

except ImportError:
    print >>sys.stderr, "Not running under uwsgi; unable to configure stack dump trigger"
except IOError:
    print >>sys.stderr, "IOError creating stack dump trigger %r" % (stack_dump_file,)
