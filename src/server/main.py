from Manager import Manager
from VideoManager import VideoManager

if __name__ == '__main__':
    manager = Manager()
    videoManager = VideoManager()
    audioManager = VideoManager(('0.0.0.0', 3978))
    manager.start()
    videoManager.start()
    audioManager.start()