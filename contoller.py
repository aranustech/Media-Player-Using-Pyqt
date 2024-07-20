from PyQt6.QtWidgets import QWidget, QMessageBox, QMainWindow
from PyQt6.QtCore import QTimer
from PyQt6 import QtGui, QtWidgets, QtCore
from ui_main import Ui_MainWindow
import cv2
import os


class Controller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect_event()
        self.showMaximized()
        self.set_stylesheet()

        self.__file_path = None
        self.cap = None
        self.video = None
        self.image = None

        self.pos_frame = 0
        self.total_frame = 0

        self.width_image = self.round_to_nearest_100(self.ui.scrollArea.width()) - 20
        self.state = "fisheye"
        self.resizeEvent = self.resize_event_new_window
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame_signal)

    def set_stylesheet(self):
        self.ui.label.setPixmap(QtGui.QPixmap("icon/VLC_Icon.svg"))
        self.ui.btn_play_pause.setIcon(QtGui.QIcon("icon/play.svg"))
        self.ui.btn_rewind.setIcon(QtGui.QIcon("icon/rewind.svg"))
        self.ui.btn_stop.setIcon(QtGui.QIcon("icon/square.svg"))
        self.ui.btn_forward.setIcon(QtGui.QIcon("icon/forward.svg"))
        self.ui.btn_change_source.setIcon(QtGui.QIcon("icon/opened_folder.svg"))
        self.ui.btn_zoom_in.setIcon(QtGui.QIcon("icon/zoom_in.svg"))
        self.ui.btn_zoom_out.setIcon(QtGui.QIcon("icon/zoom_out.svg"))

    def connect_event(self):
        self.ui.label.mousePressEvent = self.label_mouse_press_event
        self.ui.btn_zoom_in.clicked.connect(lambda: self.zoom_image("zoom_in"))
        self.ui.btn_zoom_out.clicked.connect(lambda: self.zoom_image("zoom_out"))
        self.ui.btn_change_source.clicked.connect(self.onclick_change_source)
        self.ui.btn_play_pause.clicked.connect(self.onclick_play_pause_video)
        self.ui.btn_stop.clicked.connect(self.stop_video)
        self.ui.btn_rewind.clicked.connect(self.rewind_video_5_second)
        self.ui.btn_forward.clicked.connect(self.forward_video_5_second)
        self.ui.slider_video_time.valueChanged.connect(self.set_value_change_slider)

    def resize_event_new_window(self, event):
        self.width_image = self.round_to_nearest_100(self.ui.scrollArea.width()) - 20
        self.show_image_result()

    def zoom_image(self, operation):
        if operation == "zoom_in":
            self.width_image = self.zoom_in(self.width_image)
        elif operation == "zoom_out":
            self.width_image = self.zoom_out(self.width_image)
        self.show_image_result()

    @classmethod
    def round_to_nearest_100(cls, num):
        return round(num / 20) * 20

    def label_mouse_press_event(self, event):
        if self.image is None:
            self.onclick_change_source()

    def onclick_change_source(self):
        self.timer.stop()
        option = QtWidgets.QFileDialog.Option.DontUseNativeDialog
        self.__file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Load Media", "../",
                                                                    "Files format (*.MOV *.avi *.mp4)",
                                                                    options=option)

        if self.__file_path is not None:
            self._handle_successful_media_selection(self.__file_path)

        else:
            self.show_message("Information!", "You have not selected any source!", timer=3000)

    def _handle_successful_media_selection(self, source_media):
        try:
            if source_media.endswith(('.mp4', '.MOV', '.avi')):
                self.cap = cv2.VideoCapture(source_media)
                self.pos_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                self.total_frame = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
                self.fps = self.cap.get(cv2.CAP_PROP_FPS)
                self.video = True
                self.next_frame_signal()

            else:
                self.show_message("Information!", "You have to select video file!", timer=3000)

        except Exception as e:
            print(f"Exception during select media: {e}")
            QMessageBox.warning(None, "Warning", "Cant load the history, have error in media source\n"
                                                 "Please check that your camera is on plug or \n"
                                                 "the file is exist!. you can select new media source.")
            print("some error in media_source")

    def next_frame_signal(self):
        if self.cap is not None:
            success, self.image = self.cap.read()
            if self.video:
                if success:
                    self.pos_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                    self.show_image_result()
                    duration_sec = int(self.total_frame / self.fps)
                    total_minutes = duration_sec // 60
                    duration_sec %= 60
                    total_seconds = duration_sec
                    sec_pos = int(self.pos_frame / self.fps)
                    recent_minute = int(sec_pos // 60)
                    sec_pos %= 60
                    recent_sec = sec_pos
                    self.show_timer_video_info([total_minutes, total_seconds, recent_minute, recent_sec])

                else:
                    self.timer.stop()
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.total_frame - 1)
                    _, self.image = self.cap.read()
            else:
                self.show_timer_video_info([100, 0, 0, 0])

            self.set_slider_video_time_position()
            self.show_image_result()

    def onclick_play_pause_video(self):
        if self.cap is not None:
            if self.image is not None:
                if self.ui.btn_play_pause.isChecked():
                    self.ui.btn_play_pause.setIcon(QtGui.QIcon('icon/pause.svg'))
                    self.timer.start(round(1000 / self.fps))
                else:
                    self.ui.btn_play_pause.setIcon(QtGui.QIcon('icon/play.svg'))
                    self.timer.stop()
        else:
            self.ui.btn_play_pause.setIcon(QtGui.QIcon('icon/play.svg'))

    def set_slider_video_time_position(self):
        if self.cap is not None:
            if self.video:
                try:
                    dst_value = self.pos_frame * 100 / self.total_frame
                    self.ui.slider_video_time.blockSignals(True)
                    self.ui.slider_video_time.setValue(int(dst_value))
                    self.ui.slider_video_time.blockSignals(False)

                except Exception as e:
                    print(f"Exception during slider calculation: {e}")
                    self.ui.slider_video_time.setValue(int(100))

            else:
                self.ui.slider_video_time.setValue(int(100))

    def set_value_change_slider(self, value):
        if self.cap is not None:
            if self.video:
                dst_frame = self.total_frame * value / 100
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, dst_frame)
                self.next_frame_signal()

    def show_timer_video_info(self, list_timer):
        self.ui.label_current_time.setText("%02d:%02d" % (list_timer[2], list_timer[3]))
        self.ui.label_total_time.setText("%02d:%02d" % (list_timer[0], list_timer[1]))

    def stop_video(self):
        if self.cap is not None:
            if self.video:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.timer.stop()
                self.next_frame_signal()
                self.ui.btn_play_pause.setChecked(False)
                self.onclick_play_pause_video()

    def rewind_video_5_second(self):
        if self.cap is not None:
            if self.video:
                position = self.pos_frame - 5 * self.fps
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
                self.next_frame_signal()

    def forward_video_5_second(self):
        if self.cap is not None:
            if self.video:
                position = self.pos_frame + 5 * self.fps
                if position > self.total_frame:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.total_frame - 1)
                else:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
                self.next_frame_signal()

    def show_image_result(self):
        if self.image is not None:
            self.show_image_to_label(self.ui.label, self.image, self.width_image)

    def show_image_to_label(self, label, image, width):
        h, w = image.shape[:2]
        r = width / float(w)
        height = round(h * r)
        image = cv2.resize(image, (width, height),
                           interpolation=cv2.INTER_AREA)

        label.setScaledContents(False)
        label.setMinimumSize(QtCore.QSize(width, height))
        label.setMaximumSize(QtCore.QSize(width, height))
        image = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                             QtGui.QImage.Format.Format_RGB888).rgbSwapped()
        label.setPixmap(QtGui.QPixmap.fromImage(image))

    @classmethod
    def show_message(cls, title, message, timer=5000):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.show()
        QTimer.singleShot(timer, lambda: msg.done(0))

    @staticmethod
    def zoom_in(current_size):
        if current_size > 6000:
            pass
        else:
            current_size += 100
        return current_size

    @staticmethod
    def zoom_out(current_size):
        if current_size < 640:
            pass
        else:
            current_size -= 100
        return current_size
