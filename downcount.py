import time

def dw(sec = 15,space = 2):
    for i in range(sec,0,-1):
        output = f"\r%0{space}d"
        print(output % i,end='\r')
        time.sleep(1)
    print("\r00",end='\r')

if __name__ == "__main__":
    dw(30)