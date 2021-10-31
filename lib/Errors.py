#!/usr/bin/env python3

class FrameNotFound(Exception):
    '''
        Raised when a frame name was used that does not exist in the lookup dictionary.
    '''
    def __init__(self,frame_name,message="Frame not found"):
        self.frame_name = frame_name
        self.message = message
        super().__init__(self.message)
    
    def __str__(self):
        return f'Frame [{self.frame_name}] was not found!'