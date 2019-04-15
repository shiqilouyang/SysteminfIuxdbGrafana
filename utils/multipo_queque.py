from queue import Empty
import multiprocessing

class Multipo_Queque(object):
    def __init__(self):
        self.queue = multiprocessing.JoinableQueue()
        # self.num_com = multiprocessing.cpu_count() * 2
        self.num_com = 1
        self.result_queque = multiprocessing.Queue()
        self.results = []
        self.update = None

    def Processing_Middleware(self, atitls, in_queque):
        return atitls

    def save_result_to_queque2(self, in_queque, out_queque):
        while 1:
            try:
                atitls = in_queque.get(timeout=1)
            except Empty:
                break
            results_update_from_queue =\
                self.Processing_Middleware(atitls, in_queque)
            out_queque.put(results_update_from_queue)
            in_queque.task_done()

    def run(self, data):
        self.queue.put(data)
        for _ in range(self.num_com):
            p = multiprocessing.Process(target=self.save_result_to_queque2, \
                                        args=(self.queue, self.result_queque))
            p.start()
        self.queue.join()

        while 1:
            try:
                self.update = self.result_queque.get()
                self.results.append(self.update)
                self.result_queque.get_nowait()
            except Exception:
                break
        return self.update, self.results, self.result_queque

#
# if __name__ == '__main__':
#     print(Multipo_Queque().run({"date": "su"}))