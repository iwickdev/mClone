def mClone(pathToCopyFolder, pathToCloneLocation, maxWorkerThreads):
    import os
    import sys
    import time
    import datetime
    import threading
    from shutil import copyfile

    startTime = datetime.datetime.now().timestamp()

    threadsList = []

    global fileNumber
    fileNumber = 0

    copyFolderNameSplit = list(filter(None, pathToCopyFolder.replace("\\","\\\\").split("\\")))
    copyFolderName = copyFolderNameSplit[-1]

    def dirAllFP(path):
        filesList = []
        for dirpath, subdirs, files in os.walk(path):
            for x in files:
                filesList.append(os.path.join(dirpath, x))
        return filesList
    
    def fileCopy(oldfile, newfile):
        global fileNumber

        threadsList.append(oldfile)
        try:
            copyfile(oldfile, newfile)
        except FileNotFoundError:
            os.makedirs(os.path.dirname(newfile), exist_ok=True)
            try:
                copyfile(oldfile, newfile)
            except:
                pass
        threadsList.remove(oldfile)
        fileNumber += 1

    if not os.path.exists(pathToCopyFolder) or not os.path.isdir(pathToCopyFolder):
        raise FileNotFoundError("Invalid folder: " + str(pathToCopyFolder))

    print("Preparing to clone [" + str(pathToCopyFolder) + "] ...")
    fileList = dirAllFP(pathToCopyFolder)
    for fileName in fileList:
        while len(threadsList) >= maxWorkerThreads:
            pass
        newLocation = pathToCloneLocation + "\\" + fileName.split(copyFolderName + "\\")[1]

        fileThread = threading.Thread(target=fileCopy, args=(fileName, newLocation))
        fileThread.start()

        print("Cloneing... " + str(fileNumber) + "files/of" + str(len(fileList)) + " - Running: " + str(len(threadsList)) + " theads           ", end="\r")
    
    while len(threadsList) != 0:
        print("Cloneing... " + str(fileNumber) + "files/of" + str(len(fileList)) + " - Running: " + str(len(threadsList)) + " theads           ", end="\r")
    print("Cloneing... " + str(fileNumber) + "files/of" + str(len(fileList)) + " - Running: " + str(len(threadsList)) + " theads           ", end="\r")

    print("")
    print("Cloneing... [Done] : Timelapse - " + str(round(datetime.datetime.now().timestamp() - startTime, 0)) + "seconds")

import sys
import os

def usage():
    print("\n")
    print("Usage: ")
    print("    mClone [CloneFolder] [CloneLocation]\\[FolderName] [AmountOfThreads]")
    print("    EX: mClone \"C:\\Users\\Test\\TestFolder\" \"F:\\TestFolderCopy\" 500")
    print("WARNING: Using a high number of threads can make your system slow but will increase the speed of the file copy")
    print("\n")

if len(sys.argv) == 1:
    usage()
    sys.exit()
elif sys.argv[1] == "/help":
    usage()
    sys.exit()

if not os.path.exists(sys.argv[1]):
    print("Could not locate CloneFolder Path")
    usage()
elif not os.path.exists(sys.argv[2]):
    print("Could not locate CloneLocation Path")
    usage()
elif not len(sys.argv) == 4:
    print("Invalid Arguments")
    usage()
else:
    mClone(str(sys.argv[1]), str(sys.argv[2]), int(sys.argv[3]))
