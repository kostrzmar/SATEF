#!/usr/bin/env python

import argparse
import coloredlogs, logging
from tools import PerformanceTimer
from engine import EngineFactory
import warnings

from torch.multiprocessing import Process, set_start_method,  Manager, cpu_count

try:
     set_start_method('spawn')
except RuntimeError:
    pass

warnings.filterwarnings("ignore") 
coloredlogs.install(fmt='[%(levelname)s] [%(asctime)s,%(msecs)03d] [(%(name)s[%(process)d)] [(%(threadName)s)] %(message)s', level='INFO')

parser = argparse.ArgumentParser()
parser.add_argument('-conf', required=True, help='Path to the config file')
args = parser.parse_args()

if __name__ == '__main__':
    performance_timer = PerformanceTimer("SATEF")
    EngineFactory().getEngine(args.conf).execute()
    performance_timer.stop()
