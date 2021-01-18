import threading, queue, time
# 멀티 쓰레드 사용하기

work = queue.Queue()



def display():
    while work.empty() is False:
        data = work.get()
        print(str(data))
        time.sleep(1)
        work.task_done()

# join: 일단 처리 대기를 나타냄,



data = 0
# 쓰레드의 Lock를 가져온다.
lock = threading.Lock()

def generator(start, end):
    global data
    for i in range(start, end, 1):
        # Lock이 설정된 이상 다음 이 lock를 호출 할 때 쓰레드는 대기를 한다.
        lock.acquire()
        buf = data
        time.sleep(0.01)
        data = buf +1
        print(data)
        # 사용이 끝나면 lock를 해제
        lock.release()
        # print("lock 해제")


t1 = threading.Thread(target=generator, args=(1,10))
# t2 = threading.Thread(target=generator, args=(1,10))

# start() 스레드 활동을 시작합니다.
# 스레드 객체 당 최대 한 번 호출되어야 합니다.
t1.start()
t2.start()
# 쓰레드가 종료할 때까지 대기, 호출된 스레드가 정상적으로 혹은 처리되지 않은 예외를 통해 종료,
t1.join(timeout=None)
t1.is_alive()
t2.join()
t2.is_alive()



