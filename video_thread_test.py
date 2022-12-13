import threading
import queue
import concurrent.futures
import logging
import vessel_math as vm
import capture_ocr

artery_num = 0
message_list = []
len_list = []

def cam_listener(queue, event):
    """
        Creates a watchdog thread that captures data from the ultrasound,
        and sends it to the algorithm thread via the queue
    """
    while not event.is_set():
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            ocr_thread = executor.submit(capture_ocr.capture_decoder)
            return_value = ocr_thread.result()
        thread_return = str(return_value).split(",")
        #logging.info("cam_listener is active")
        return_string = ""
        #logging.info("recieved from thread: %s",thread_return)
        for i in range(len(thread_return)):
            try:
                return_float = float(thread_return[i])
                logging.info("recieved from thread: %f",return_float)
                found = True
                
            except:
                if thread_return[i] == ".":
                    return_string += thread_return[i]

        if found == True:            
            queue.put( return_float, "Camera")

def alg_store(queue, event):
    """
        takes the information captured by the ocr thread, 
        and runs it through Dr. Busell's algorithm
    """
    while not event.is_set() or not queue.empty():
        message = queue.get()
        if len(message_list) < 5:
            message_list.append(message)
            #logging.info("alg_store is active: %f", message)
        else:
            #logging.info("alg_store is active")
            if len(len_list) == 51:
                event.set()
            logging.info("run through the algorithm: %s",message_list)
            algThread = threading.Thread(target=patient_instance.converter, args=(message_list,))
            algThread.start()
            algThread.join()
            message_list.clear()
            len_list.append("i")
            message_list.append(len(len_list))
            
            

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    patient_instance = vm.Vessel_math("DavidsonLiam")
    message_list.append(len(len_list))
    pipeline = queue.Queue(maxsize=10)
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(cam_listener, pipeline, event)
        executor.submit(alg_store, pipeline, event)

    logging.info("done")

    vessel_group_var = patient_instance.macro_vessel_calculations()

    print(vessel_group_var)