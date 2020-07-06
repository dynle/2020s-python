from multiprocessing import Process, Queue
import time
import logging
import os
import math
import asyncio
from quart import Quart, request, url_for, jsonify, render_template

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S', level=logging.INFO)

def find_primes(q_in,q_out):
    logging.info("start finding primes")
    low, high = q_in.get()
    primes = []
    if low % 2 == 0:
        low += 1
    for n in range(low, high, 2):
        mid = int(math.sqrt(n)) + 1
        for p in range(2, mid):
            if n % p == 0:
                break
        else:
            primes.append(n)
    logging.info(f"from {low} to {high} are {primes}")
    q_out.put(primes)

if __name__ == '__main__':
    app = Quart(__name__)

    process_result = None

    @app.route("/start/")
    async def start():
        global process_result

        #restart
        if process_result and not process_result.is_alive():
            process_result.join()
            process_result = None

        if not process_result:
            global results
            q_args = Queue()
            q_res = Queue()            
            process_result = Process(target=find_primes, args=(q_args,q_res))
            process_result.start()
            q_args.put((1,200))
            results = q_res.get()
            return jsonify({"result":"success"})
        else:
            return jsonify({"result":"fail"})

    @app.route("/result/")
    async def result():
        return jsonify(f"primes : {results}")
    
    app.run()