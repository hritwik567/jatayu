import dockerstr as ds
import time
def check_queue_status():
    while 1:
        print("1")
        if not ds.dockerde:
            time.sleep(5)
        else:
            func_uuid=ds.dockerde.popleft
            ds.image_create_handler(func_uuid=func_uuid)
if __name__=='__main__':
    check_queue_status()