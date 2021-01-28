import logging
import time

class PerformanceTimer():


    def __init__(self, timerName, startAlready=True):      
        self.timer_name = timerName
        self.start_time = 0
        self.end_time = 0
        if startAlready:
            self.start()
        super().__init__() 

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()
        time_diff = self.end_time - self.start_time
        logging.info("Total processing time for [%s] -> %d min %f sec" % (self.timer_name, int(time_diff / 60), time_diff % 60))

    


