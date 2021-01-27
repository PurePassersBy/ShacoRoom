from Manager import Manager
from VideoManager import VideoManager
from ResourceManager import ResourceManager

SERVER_ADDRESS = ('0.0.0.0', 3976)
VIDEO_SERVER_ADDRESS = ('0.0.0.0', 3977)
AUDIO_SERVER_ADDRESS = ('0.0.0.0', 3978)
RESOURCE_SERVER_ADDRESS = ('0.0.0.0', 3979)


if __name__ == '__main__':
    manager = Manager(SERVER_ADDRESS)
    videoManager = VideoManager(VIDEO_SERVER_ADDRESS)
    audioManager = VideoManager(AUDIO_SERVER_ADDRESS)
    resourceManager = ResourceManager(RESOURCE_SERVER_ADDRESS)
    manager.start()
    videoManager.start()
    audioManager.start()