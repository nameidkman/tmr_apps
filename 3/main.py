import sys

import gi
from PySide6 import QtCore, QtGui, QtWidgets

gi.require_version("Gst", "1.0")
from gi.repository import Gst

Gst.init(None)

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 640


class MyWidget(QtWidgets.QWidget):
    def __init__(self):

        super().__init__()
        self.cam_width = CAMERA_WIDTH
        self.cam_height = CAMERA_HEIGHT

        # makign the main camera for one side
        # on the left side of the split screen
        self.camera = QtWidgets.QLabel()
        self.camera.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.camera.setScaledContents(True)

        # similar setting for the right side
        # which is going to play a video
        self.video_player = QtWidgets.QLabel()
        self.video_player.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.video_player.setScaledContents(True)

        # layout

        self.layout = QtWidgets.QGridLayout()
        self.layout.addWidget(self.camera, 0, 0)
        self.layout.addWidget(self.video_player, 0, 1)
        self.layout.setRowStretch(0, 1)
        self.layout.setColumnStretch(0, 0)
        self.layout.setColumnStretch(1, 1)

        self.setLayout(self.layout)

        self.start_camera_pipeline()
        self.start_video_pipeline()

    def start_camera_pipeline(self):
        # you convert the video input into x raw so that u can set a specific width and height
        # then after that you convert it into rgb so that you are able to show it into the screen in color
        pipeline_str = (
            f"mfvideosrc device-index=0 ! videoconvert ! "
            f"videoscale ! video/x-raw, width={self.cam_width}, height={self.cam_height} ! "
            f"videoconvert ! video/x-raw, format=RGB ! "
            f"appsink name=cam_sink emit-signals=true max-buffers=1 drop=true"
        )

        try:
            self.cam_pipeline = Gst.parse_launch(pipeline_str)
        except Exception as e:
            print(f"camera parsing prblem: {e}")
            self.cam_pipeline = None
            return

        # setting up the sink
        sink = self.cam_pipeline.get_by_name("cam_sink")
        if sink:
            sink.connect("new-sample", self.on_new_sample, self.camera)

        bus = self.cam_pipeline.get_bus()
        bus.add_signal_watch()

        ret = self.cam_pipeline.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.FAILURE:
            print("Camera pipeline failed to start.")

    def start_video_pipeline(self):
        VIDEO_URI = (
            "https://gstreamer.freedesktop.org/data/media/sintel_trailer-480p.webm"
        )

        # GstBin groups several elements so playbin sees one "video sink" unit.
        sink_bin = Gst.Bin.new("video_sink_bin")

        # videoconvert: colour-space conversion (YUV/NV12/etc. → RGB)
        convert = Gst.ElementFactory.make("videoconvert", "vc")
        # videoscale: resize to our target resolution
        scale = Gst.ElementFactory.make("videoscale", "vs")
        # appsink: fires "new-sample" signal into Python per frame
        appsink = Gst.ElementFactory.make("appsink", "web_sink")

        appsink.set_property("emit-signals", True)
        appsink.set_property("max-buffers", 1)
        appsink.set_property("drop", True)

        # Caps lock the appsink to exactly the format our QImage code expects.
        caps = Gst.Caps.from_string(
            f"video/x-raw, format=RGB, width={self.cam_width}, height={self.cam_height}"
        )
        appsink.set_property("caps", caps)

        sink_bin.add(convert)
        sink_bin.add(scale)
        sink_bin.add(appsink)
        convert.link(scale)
        scale.link(appsink)

        # GhostPad: a proxy pad on the bin's exterior that playbin will connect
        # its decoded video stream to.
        ghost_pad = Gst.GhostPad.new("sink", convert.get_static_pad("sink"))
        sink_bin.add_pad(ghost_pad)

        # building and creating the custom sink
        self.web_pipeline = Gst.ElementFactory.make("playbin", "player")
        self.web_pipeline.set_property("uri", VIDEO_URI)
        self.web_pipeline.set_property("video-sink", sink_bin)

        # connect the frame
        appsink.connect("new-sample", self.on_new_sample, self.video_player)

        bus = self.web_pipeline.get_bus()
        bus.add_signal_watch()
        ret = self.web_pipeline.set_state(Gst.State.PLAYING)
        if ret == Gst.StateChangeReturn.FAILURE:
            print("Web video pipeline failed to start.")

    def on_new_sample(self, sink, target_label):
        # there inorder to conecter the raw RGB bytes to Qimage to Qpixmap
        # and then finally being able to add it to qt main thrad
        sample = sink.emit("pull-sample")
        if not sample:
            return Gst.FlowReturn.ERROR

        buf = sample.get_buffer()
        success, map_info = buf.map(Gst.MapFlags.READ)
        if not success:
            return Gst.FlowReturn.ERROR

        try:
            q_imag = QtGui.QImage(
                map_info.data,
                self.cam_width,
                self.cam_height,
                self.cam_width * 3,
                QtGui.QImage.Format.Format_RGB888,
            )
            # copying before the buffer is unmapped
            pixmap = QtGui.QPixmap.fromImage(q_imag.copy())

            QtCore.QMetaObject.invokeMethod(
                target_label,
                "setPixmap",
                QtCore.Qt.ConnectionType.QueuedConnection,
                QtCore.Q_ARG(QtGui.QPixmap, pixmap),
            )
        finally:
            buf.unmap(map_info)
        return Gst.FlowReturn.OK


if __name__ == "__main__":
    # init the application
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.resize(1280, 540)
    widget.show()

    # killing the app so that there is no memory leak
    sys.exit(app.exec())
