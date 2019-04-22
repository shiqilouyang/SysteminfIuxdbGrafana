import os, subprocess, tempfile, time

class OSUtil(object):
    @staticmethod
    def run_linux(dos, asyn=True):
        if asyn:
            subprocess.Popen(dos, shell=True)
        else:
            rc = subprocess.Popen(dos, shell=True)
            rc.wait()

    @staticmethod
    def safe_popen(cmd, timeout=0, interval=10, **params):
        interval = interval
        # to get a temp file Name from system
        fd1, fn1 = tempfile.mkstemp(suffix='.log', prefix='test_stdout_')
        fd2, fn2 = tempfile.mkstemp(suffix='.log', prefix='test_stderr_')
        os.close(fd1)
        os.close(fd2)
        f1 = None
        f2 = None
        try:
            rc = None
            pobj = subprocess.Popen(cmd, stdout=open(fn1, 'w'), stderr=open(fn2, 'w'))
            if timeout > 0:
                start = time.time()
                # Check if the child process is finished and return the status!
                # it return None when it down
                rc = pobj.poll()
                while rc is None:  # loop if process is still running
                    if timeout < time.time() - start:
                        pobj.kill()
                        break
                    # Check every 10 seconds when job long ago
                    time.sleep(interval)
                    rc = pobj.poll()
            else:
                rc = pobj.wait()

            outstr, errstr = '', ''
            try:
                f1 = open(fn1)
                line = f1.readline()
                while line:
                    outstr += line
                    line = f1.readline()
                f1.close()
                f1 = None
                os.remove(fn1)

                f2 = open(fn2)
                line = f2.readline()
                while line:
                    errstr += line
                    line = f2.readline()
                f2.close()
                f2 = None
                os.remove(fn2)
            except Exception:
                pass
            # with open()
            return rc, outstr, errstr
        finally:
            if f1 is not None:
                f1.close()
            if f2 is not None:
                f2.close()

# import threading
# g_jobop_lock = threading.RLock()
# g_jobop_lock.acquire()
# execmd = ["python",'multipo_queque.py']
# OSUtil.safe_popen(execmd)
# g_jobop_lock.release()