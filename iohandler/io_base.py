import threading
from multiprocessing import Queue
import queue

class IOBase:
    reader = None
    writer = None
    serial = None
    read_queue = None
    write_queue = None

    def __init__(self, read_queue):
        self.read_queue = read_queue
        self.write_queue = Queue(10)
        self.reader = threading.Thread(target=self.reader_thread)
        self.reader.daemon = True
        self.reader.start()
        self.writer = threading.Thread(target=self.writer_thread)
        self.writer.daemon = True
        self.writer.start()

    def reader_thread(self):
        raise NotImplementedError()

    def writer_thread(self):
        raise NotImplementedError()

    def writeline(self, line):
        try:
            self.write_queue.put_nowait(line + '\n')
        except queue.Full:
            #TODO alert somehow without flooding?
            pass
