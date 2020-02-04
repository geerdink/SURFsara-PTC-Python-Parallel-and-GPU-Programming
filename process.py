import os
from multiprocessing import Process, Pool

def doubler(number):
    result = number * 2
    pid = os.getpid()
    print(f'Multiplying {number} on proc ID {pid}')
    return result

if __name__ == '__main__':
    numbers = [5,10,20]
    # procs = []
    # for index, number in enumerate(numbers):
    #     proc = Process(target=doubler)
    #     procs.append(proc)
    #     proc.start()
    
    # for proc in procs:
    #     proc.join()

    # wait until everyting ends
    pool = Pool(processes=3)
    print(pool.map(doubler, numbers))

    print('Done')

    # same behaviour as daemon threads
    result = pool.apply_async(doubler, [25])
    print(result.get(timeout=1))

    print('Done')
