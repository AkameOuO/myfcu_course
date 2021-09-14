import time

def dw(sec = 15,space = 2):
    for i in range(sec,0,-1):
        time.sleep(1)

if __name__ == "__main__":
    dw(30)