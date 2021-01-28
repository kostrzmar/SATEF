from pathlib import Path
import os

def getNumberOfLines(file_name):
    num_lines = 0
    with open(file_name) as f:
        #num_lines = sum(1 for line in f if line.rstrip())
        num_lines = sum(1 for line in f)
    return num_lines


def getParentPath(file_name):
    head, __ = os.path.split(file_name)
    return head

def getFileFromPath(file_name):
    __, tail = os.path.split(file_name)
    return tail

def getFullPath(folder_name, file_name):
    return os.path.join(folder_name, file_name)

def isFileExist(file):
    return os.path.isfile(file)

def removeIfExit(canBeRemoved):
    if os.path.isfile(canBeRemoved):
        os.remove(canBeRemoved)

def readFileToArray(file_name):
    out = []
    with open(file_name,"r") as f:
        for i in f.readlines():
            if not i.strip():
                continue
            if i:
                out.append(i.strip())
    return out
