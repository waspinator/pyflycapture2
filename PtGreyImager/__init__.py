#!/usr/bin/python

import flycapture2 as fc2
import numpy as np
import time

class PtgreyImager(object):
    """
    Example class for handling init, imaging, and shutdown of a PtGrey Flea3 camera
    """
    def __init__(self, idx=0):
        """
        :param idx: Camera ID to use
        :return:
        """
        self.img = np.zeros((4000,3000,3)) # Keep a copy of the current working image, init to zeros
        self.ctx = fc2.Context()

        # assume only one camera
        self.ctx.connect(*self.ctx.get_camera_from_index(idx))

        # Set to Format7, mode 10, RAW8 pixels. This captures raw bayer images at the highest resolution
        self.ctx.set_format7_configuration(fc2.MODE_10, 0, 0, 4000, 3000, fc2.PIXEL_FORMAT_RAW8)

        # validates necessary for some reason? 
        m, f = self.ctx.get_video_mode_and_frame_rate()
        p = self.ctx.get_property(fc2.AUTO_EXPOSURE)
        p['auto_manual_mode'] = False
        self.ctx.set_property(**p)

        return

    def shutdown(self):
        """
        Shutdown the camera
        :return:
        """
        try:
            self.stop()
            self.ctx.disconnect()
        except fc2.ApiError:
            pass
        return

    def start(self):
        """
        Start capturing
        :return:
        """
        self.ctx.start_capture()
        return

    def stop(self):
        """
        Stop capturing
        :return:
        """
        self.ctx.stop_capture()
        return

    def getimg(self):
        """
        Get an image from the camera.
        Transposes the image for easy viewing
        Image is buffered in self.img.
        :return:
        """
        self.im = fc2.Image()
        self.img = np.transpose(np.array(self.ctx.retrieve_buffer(self.im)))
        return self.img

    def shutter(self, ms):
        """
        Set the camera shuttering
        :param ms: Shutter time in ms
        :return:
        """
        if type(ms) is not float and type(ms) is not int:
            raise(TypeError, "Requires float/int input")

        p = self.ctx.get_property(fc2.SHUTTER)
        p['abs_value'] = ms
        p['auto_manual_mode'] = False
        self.ctx.set_property(**p)
        return self.ctx.get_property(fc2.SHUTTER)['abs_value']

    def gain(self, db):
        """
        Set the camera gain
        :param db: Shutter gain in dB
        :return:
        """
        if type(db) is not float and type(db) is not int:
            raise(TypeError, "Requires float/int input")

        p = self.ctx.get_property(fc2.GAIN)
        p['abs_value'] = db
        p['auto_manual_mode'] = False
        self.ctx.set_property(**p)
        return self.ctx.get_property(fc2.GAIN)['abs_value']

    def framerate(self, fps):
        """
        Set the camera framerate"
        :param fps: Camera framerate in FPS, flat
        :return:
        """
        if type(fps) is not float:
            raise(TypeError, "Requires float")

        p = self.ctx.get_property(fc2.FRAME_RATE)
        p['abs_value'] = fps
        p['auto_manual_mode'] = False
        self.ctx.set_property(**p)
        return self.ctx.get_property(fc2.FRAME_RATE)['abs_value']


# example code, interactive with pyqtgraph output
if __name__ == '__main__':
    x = PtgreyImager()
    x.start()

    x.shutter(50)
    x.gain(2)

    import pyqtgraph as pg
    img = x.getimg()
    i = pg.image(img)

    import IPython
    print "img: Current image object"
    print "x: opern camera object"
    print "i: pyqtgraph image handle"
    print "i.setImage(x.getimg()) should refresh the display"

    IPython.embed()

    x.shutdown()

