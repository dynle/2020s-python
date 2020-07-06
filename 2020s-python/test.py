from multiprocessing import Process, Queue
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S', level=logging.INFO)

def f(q):
    q.put([42, None, 'hello'])

if __name__ == '__main__':
    q = Queue()
    print(q)
    p = Process(target=f, args=(q,))
    p.start()
    logging.info("result :{}".format(q.get()))
    p.join()