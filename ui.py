import glob
import os
import pickle
import subprocess
import sys
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog, QMessageBox, QDialog, QWidget, \
    QVBoxLayout, QHBoxLayout, QLabel, QDialogButtonBox, QCheckBox, QRadioButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from benchmark import feed_to_visual


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("FD Production Suite")

        # Set window size based on user screen resolution
        self.width, self.height = 1600, 900
        self.top, self.left = int((U_WIDTH - self.width) / 2), int((U_HEIGHT - self.height) / 2)  # screen-centered
        self.setGeometry(self.top, self.left, self.width, self.height)  # top, left, width, height

        # Attributes
        cwd = os.getcwd()
        self.traces_dir = os.path.join(cwd, 'data') if os.path.exists('data') else None
        self.extension_dir = os.path.join(cwd, 'Extension') if os.path.exists('Extension') else None
        self.record_file = os.path.join(cwd, 'Extension\\record.py') if os.path.exists('Extension\\record.py') else None
        self.score_file = None
        self.last_directory = cwd  # last selected directory by user

        # Children widgets
        self.msg_dialog = MainWindowDialog()
        self.benchmark_window = None
        self.plot_window = None

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        benchmark_container = QWidget()
        benchmark_container_layout = QVBoxLayout()

        traces_dir_container = QWidget()
        traces_dir_container_layout = QHBoxLayout()
        get_traces_dir_button = QPushButton("select")
        get_traces_dir_button.clicked.connect(self.on_get_traces_dir)
        get_traces_dir_button.setMaximumSize(120, 45)
        traces_dir_container_layout.addWidget(get_traces_dir_button)
        self.traces_dir_label = QLabel(f"Traces folder: {self.traces_dir if self.traces_dir else '(not selected)'}")
        traces_dir_container_layout.addWidget(self.traces_dir_label)
        traces_dir_container_layout.setAlignment(Qt.AlignCenter)
        traces_dir_container.setLayout(traces_dir_container_layout)

        benchmark_container_layout.addWidget(traces_dir_container)

        extension_dir_container = QWidget()
        extension_dir_container_layout = QHBoxLayout()

        get_extension_dir_button = QPushButton("select")
        get_extension_dir_button.clicked.connect(self.on_get_extension_dir)
        get_extension_dir_button.setMaximumSize(120, 45)
        extension_dir_container_layout.addWidget(get_extension_dir_button)
        self.extension_dir_label = QLabel(f"Extension folder: "
                                          f"{self.extension_dir if self.extension_dir else '(not selected)'}")
        extension_dir_container_layout.addWidget(self.extension_dir_label)
        extension_dir_container_layout.setAlignment(Qt.AlignCenter)
        extension_dir_container.setLayout(extension_dir_container_layout)

        benchmark_container_layout.addWidget(extension_dir_container)

        self.detected_fd_label = QLabel(f"Detected FD(s): {' '.join(self.search_for_fd(self.extension_dir))}")
        benchmark_container_layout.addWidget(self.detected_fd_label)

        record_file_container = QWidget()
        record_file_container_layout = QHBoxLayout()
        get_record_file_button = QPushButton("select")
        get_record_file_button.clicked.connect(self.on_get_record_file)
        get_record_file_button.setMaximumSize(120, 45)
        record_file_container_layout.addWidget(get_record_file_button)
        self.record_file_label = QLabel(f"Record file: {self.record_file if self.record_file else '(not selected)'}")
        record_file_container_layout.addWidget(self.record_file_label)
        record_file_container_layout.setAlignment(Qt.AlignCenter)
        record_file_container.setLayout(record_file_container_layout)

        benchmark_container_layout.addWidget(record_file_container)

        rb_button_widget = QWidget()
        rb_button_layout = QHBoxLayout()
        run_benchmark_button = QPushButton("Run Benchmark")
        run_benchmark_button.clicked.connect(self.toggle_benchmark_window)
        run_benchmark_button.setMaximumWidth(200)
        rb_button_layout.addWidget(run_benchmark_button)
        rb_button_widget.setLayout(rb_button_layout)

        benchmark_container_layout.addWidget(rb_button_widget)

        benchmark_container_layout.setAlignment(Qt.AlignCenter)
        benchmark_container.setLayout(benchmark_container_layout)
        main_layout.addWidget(benchmark_container)

        dividing_line = QLabel("-" * 120)
        main_layout.addWidget(dividing_line)

        plot_container = QWidget()
        plot_container_layout = QVBoxLayout()

        score_file_container = QWidget()
        score_file_container_layout = QHBoxLayout()
        get_score_file_button = QPushButton("select")
        get_score_file_button.clicked.connect(self.on_get_score_file)
        get_score_file_button.setMaximumSize(120, 45)
        score_file_container_layout.addWidget(get_score_file_button)
        self.score_file_label = QLabel(f"Score file: {self.score_file if self.score_file else '(not selected)'}")
        score_file_container_layout.addWidget(self.score_file_label)
        score_file_container_layout.setAlignment(Qt.AlignCenter)
        score_file_container.setLayout(score_file_container_layout)

        plot_container_layout.addWidget(score_file_container)

        plot_button_widget = QWidget()
        plot_button_layout = QHBoxLayout()
        plot_button = QPushButton("Plot from File")
        plot_button.clicked.connect(self.toggle_plot_window)
        plot_button.setMaximumWidth(200)
        plot_button_layout.addWidget(plot_button)
        plot_button_widget.setLayout(plot_button_layout)

        plot_container_layout.addWidget(plot_button_widget)

        plot_container_layout.setAlignment(Qt.AlignCenter)
        plot_container.setLayout(plot_container_layout)
        main_layout.addWidget(plot_container)

        main_layout.setAlignment(Qt.AlignCenter)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        self.show()

    # search for failure detectors (.txt files) in a directory
    # blocking, can take a long time if directory is large
    def search_for_fd(self, dir_):
        if dir_:
            path_name = os.path.join(dir_, '*.txt')
            results = glob.glob(path_name)
            failure_detectors = [os.path.basename(f).split('.')[0] for f in results]
            return failure_detectors
        return []

    def on_get_traces_dir(self):
        file_dir = QFileDialog.getExistingDirectory(self, "Select traces folder", self.last_directory)
        if file_dir:
            self.traces_dir = file_dir
            self.traces_dir_label.setText(f"Traces folder: {file_dir}")
            self.last_directory = os.path.dirname(file_dir)

    def on_get_extension_dir(self):
        file_dir = QFileDialog.getExistingDirectory(self, "Select Extension folder", self.last_directory)
        if file_dir:
            self.extension_dir = file_dir
            self.extension_dir_label.setText(f"Extension folder: {file_dir}")
            self.last_directory = os.path.dirname(file_dir)
            self.detected_fd_label.setText(f"Detected FD(s): {' '.join(self.search_for_fd(file_dir))}")

    def on_get_record_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file", self.last_directory, "Python files (*.py)")
        if file_path:
            self.record_file = file_path
            self.record_file_label.setText(f"Record file: {file_path}")

    def toggle_benchmark_window(self):
        if self.benchmark_window and self.benchmark_window.isVisible():
            self.msg_dialog.display_error("You can at most open one benchmark window at a time!")
            return
        if (not self.traces_dir) or (not self.extension_dir) or (not self.record_file):
            self.msg_dialog.display_error("Please select all traces folder, Extension folder and Record file first!")
            return
        self.benchmark_window = BenchmarkWindow(parent=self)
        self.benchmark_window.show()

    def on_get_score_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file", self.last_directory, "MyData files (*.mydata)")
        if file_path:
            self.score_file = file_path
            self.score_file_label.setText(f"Score file: {file_path}")

    def toggle_plot_window(self):
        if self.plot_window and self.plot_window.isVisible():
            self.msg_dialog.display_error("You can at most open one plot window at a time!")
            return
        if not self.score_file:
            self.msg_dialog.display_error("Please select benchmark score file first!")
            return
        try:
            with open(self.score_file, "rb") as f:
                data = pickle.load(f)
            self.plot_window = PlotWindow(data, parent=self)
            self.plot_window.show()
        except Exception as e:
            self.msg_dialog.display_error(e)


class MainWindowDialog(QMessageBox):

    def __init__(self):
        super().__init__()

        self.setStandardButtons(QMessageBox.Ok)

    def display_message(self, msg, title, level=QMessageBox.Information):
        # "level" can be QMessageBox.Question / Information / Warning / Critical
        self.setIcon(level)
        self.setWindowTitle(title)
        self.setText(str(msg))
        self.exec_()

    def display_error(self, err_msg_or_exception):
        return self.display_message(str(err_msg_or_exception), "Error", QMessageBox.Critical)


class BenchmarkWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__()

        self.setWindowTitle("Benchmark")
        self.setMinimumWidth(480)
        self.setMinimumHeight(270)
        self.parent = parent

        # Children widgets
        self.quit_window = None
        self.data_not_saved_window = None
        self.plot_window = None  # main window can have another one

        layout = QVBoxLayout()

        self.main_label = QLabel("Running... 0")
        layout.addWidget(self.main_label)

        buttons_widgets = QWidget()
        buttons_layout = QHBoxLayout()

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_benchmark_score)
        self.save_button.hide()
        buttons_layout.addWidget(self.save_button)

        self.plot_button = QPushButton("Plot")
        self.plot_button.clicked.connect(self.toggle_plot_window)
        self.plot_button.hide()
        buttons_layout.addWidget(self.plot_button)

        self.close_button = QPushButton("Cancel")
        self.close_button.clicked.connect(self.on_close_window)
        buttons_layout.addWidget(self.close_button)

        buttons_layout.setAlignment(Qt.AlignCenter)
        buttons_widgets.setLayout(buttons_layout)
        layout.addWidget(buttons_widgets)

        # Timer
        self.time_elapsed = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_time_elapsed)
        self.timer.start()

        # Worker thread
        self.is_finished = False
        self.is_cancelled = False
        self.is_data_saved = False
        self.benchmark_score = {}  # also the input to visualization
        self.worker_thread = WorkerThread(parent=self)
        self.worker_thread.signals.finished.connect(self.on_thread_finish)
        self.worker_thread.signals.result.connect(self.handle_thread_result)
        self.worker_thread.signals.error.connect(self.handle_thread_error)
        self.worker_thread.start()

        layout.setSpacing(50)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def update_time_elapsed(self):
        self.time_elapsed += 1
        self.main_label.setText(f"Running... {self.time_elapsed}")

    def on_thread_finish(self):
        self.is_finished = True
        self.timer.stop()
        if self.is_cancelled:
            self.main_label.setText("Benchmark cancelled")
        else:
            self.main_label.setText(f"Finished. Benchmark score ready.")
            self.save_button.show()
            self.plot_button.show()
        self.close_button.setText("Close")
        if self.quit_window:  # if quit window exists, close it
            QTimer.singleShot(0, self.quit_window.close)

    def handle_thread_result(self, result):
        self.benchmark_score = result

    def handle_thread_error(self, error):
        self.parent.msg_dialog.display_error(error)

    def on_close_window(self):
        if not self.is_finished:
            self.quit_window = BenchmarkQuitWindow(parent=self)
            self.quit_window.show()
        elif (not self.is_data_saved) and (not self.is_cancelled):
            self.data_not_saved_window = BenchmarkDataNotSavedWindow(parent=self)
            self.data_not_saved_window.show()
        else:
            QTimer.singleShot(0, self.close)

    def save_benchmark_score(self):
        default_path = os.path.join(self.parent.last_directory,
                                    f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')}.mydata")
        file_path, _ = QFileDialog.getSaveFileName(self, "Save benchmark score", default_path,
                                                   "MyData files (*.mydata)")
        if file_path:
            with open(file_path, "wb") as f:
                pickle.dump(self.benchmark_score, f)
            self.is_data_saved = True
            self.parent.last_directory = os.path.dirname(file_path)
            self.parent.msg_dialog.display_message(f'Benchmark score saved as "{file_path}"', "Data saved")

    def toggle_plot_window(self):
        if self.plot_window and self.plot_window.isVisible():
            self.msg_dialog.display_error("You can at most open one plot window at a time!")
            return
        data = self.benchmark_score
        self.plot_window = PlotWindow(data, parent=self.parent)  # set parent for displaying messages
        self.plot_window.show()

    def closeEvent(self, event):
        if not self.is_finished:
            event.ignore()
            self.on_close_window()
        else:
            event.accept()


class BenchmarkQuitWindow(QDialog):
    # Displayed when user tries to close the window while benchmark is still running

    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent
        self.setWindowTitle("Confirm quit")

        layout = QVBoxLayout()

        label = QLabel("Benchmark is still running. Are you sure to quit?")
        layout.addWidget(label)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        self.button_box.clicked.connect(self.on_button_click)
        layout.addWidget(self.button_box)

        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def on_button_click(self, button_clicked):
        button_clicked = QDialogButtonBox.standardButton(self.button_box, button_clicked)
        if button_clicked == QDialogButtonBox.Yes:
            proc = self.parent.worker_thread.proc
            proc.kill()
            proc.returncode = 777  # we define the return code of benchmark process to be shut down as 777
            self.parent.is_cancelled = True
        QTimer.singleShot(0, self.close)


class BenchmarkDataNotSavedWindow(QDialog):

    def __init__(self, parent=None):
        super().__init__()

        self.setWindowTitle("Data not saved")
        self.parent = parent

        layout = QVBoxLayout()

        label = QLabel("Benchmark score has not been saved. Are you sure to quit?")
        layout.addWidget(label)
        self.button_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        self.button_box.clicked.connect(self.on_button_click)
        layout.addWidget(self.button_box)

        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def on_button_click(self, button_clicked):
        button_clicked = QDialogButtonBox.standardButton(self.button_box, button_clicked)
        if button_clicked == QDialogButtonBox.Yes:
            QTimer.singleShot(0, self.parent.close)
        QTimer.singleShot(0, self.close)


class WorkerSignals(QObject):
    finished = pyqtSignal()
    result = pyqtSignal(object)
    error = pyqtSignal(object)


class WorkerThread(QThread):

    def __init__(self, parent=None):
        super().__init__()

        self.parent = parent
        self.signals = WorkerSignals()
        self.proc = None

    def run(self):
        # TODO: self.parent.parent is a dangerous design because of consistency problem
        self.proc = subprocess.Popen(["python", "run_benchmark.py",
                                      "-t", self.parent.parent.traces_dir,
                                      "-E", self.parent.parent.extension_dir,
                                      "-R", self.parent.parent.record_file],
                                     stdout=subprocess.PIPE)
        stdout, stderr = self.proc.communicate()
        if self.proc.returncode == 0:
            benchmark_data = pickle.loads(stdout)
            benchmark_score = {}
            for algo, data in benchmark_data.items():
                feed_to_visual(algo, data, benchmark_score)
            self.signals.result.emit(benchmark_score)
        elif self.proc.returncode != 777:  # 777 is the return code when user kills the process in quit window
            self.signals.error.emit(stderr)
        self.signals.finished.emit()


class PlotWindow(QWidget):

    def __init__(self, data, parent=None):
        super().__init__()

        self.setWindowTitle("Plot")
        self.setMinimumWidth(1920)
        self.setMinimumHeight(1080)

        # Attributes
        self.parent = parent
        self.data = data  # benchmark score
        self.failure_detectors = []  # check boxes
        self.metrics = []  # check boxes

        layout = QVBoxLayout()

        upper_widget = QWidget()
        upper_layout = QHBoxLayout()

        h_bar_chart_button = QRadioButton("Horizontal bar chart")
        h_bar_chart_button.setChecked(True)  # set h-bar chart button checked first
        h_bar_chart_button.toggled.connect(self.toggle_h_bar_chart)
        upper_layout.addWidget(h_bar_chart_button)

        line_chart_button = QRadioButton("Line chart")
        line_chart_button.toggled.connect(self.toggle_line_chart)
        upper_layout.addWidget(line_chart_button)

        upper_layout.setAlignment(Qt.AlignCenter)
        upper_widget.setLayout(upper_layout)

        layout.addWidget(upper_widget)

        central_widget = QWidget()
        central_layout = QHBoxLayout()

        fd_widget = QWidget()
        fd_widget_layout = QVBoxLayout()

        for fd in self.data.keys():
            check_box = QCheckBox()
            check_box.setText(fd)  # fd = check_box.text()
            check_box.setChecked(True)
            check_box.toggled.connect(self.draw_and_redraw)
            self.failure_detectors.append(check_box)
            fd_widget_layout.addWidget(check_box)

        fd_widget_layout.setAlignment(Qt.AlignCenter)
        fd_widget.setLayout(fd_widget_layout)
        central_layout.addWidget(fd_widget)

        self.h_bar_chart_canvas = MyCanvas(16, 9, 120)
        central_layout.addWidget(self.h_bar_chart_canvas)

        self.line_chart_canvas = MyCanvas(16, 9, 120)
        self.line_chart_canvas.hide()  # hide line chart first
        central_layout.addWidget(self.line_chart_canvas)

        metric_widget = QWidget()
        metric_widget_layout = QVBoxLayout()

        for metric in self.data.values().__iter__().__next__().keys():
            check_box = QCheckBox()
            check_box.setText(metric)  # metric = check_box.text()
            check_box.setChecked(True)
            check_box.toggled.connect(self.draw_and_redraw)
            self.metrics.append(check_box)
            metric_widget_layout.addWidget(check_box)

        metric_widget_layout.setAlignment(Qt.AlignCenter)
        metric_widget.setLayout(metric_widget_layout)
        central_layout.addWidget(metric_widget)

        central_layout.setAlignment(Qt.AlignCenter)
        central_widget.setLayout(central_layout)
        layout.addWidget(central_widget)

        lower_widget = QWidget()
        lower_layout = QHBoxLayout()
        self.save_h_bar_chart_button = QPushButton("Save Figure")
        self.save_h_bar_chart_button.setMaximumWidth(200)
        self.save_h_bar_chart_button.clicked.connect(self.save_h_bar_chart)
        lower_layout.addWidget(self.save_h_bar_chart_button)

        self.save_line_chart_button = QPushButton("Save Figure")
        self.save_line_chart_button.setMaximumWidth(200)
        self.save_line_chart_button.clicked.connect(self.save_line_chart)
        self.save_line_chart_button.hide()  # hide line chart's "save" button first
        lower_layout.addWidget(self.save_line_chart_button)

        lower_widget.setLayout(lower_layout)
        layout.addWidget(lower_widget)

        layout.setAlignment(Qt.AlignVCenter)
        self.setLayout(layout)
        self.draw_and_redraw()

    # NOTE: this is blocking and could cause GUI to freeze, but since there's nothing much else you can do even if it is
    # non-blocking, I do not implement it
    def draw_and_redraw(self):
        # find fd and metrics that are checked and draw them
        active_fd = []
        for fd in self.failure_detectors:
            if fd.isChecked():
                active_fd.append(fd.text())
        active_metrics = []
        for metric in self.metrics:
            if metric.isChecked():
                active_metrics.append(metric.text())
        # draw charts
        df = pd.DataFrame(self.data)[active_fd].loc[active_metrics]
        self.h_bar_chart_canvas.h_bar_chart(df)
        self.line_chart_canvas.line_chart(df)

    def toggle_h_bar_chart(self):
        self.line_chart_canvas.hide()
        self.save_line_chart_button.hide()
        self.h_bar_chart_canvas.show()
        self.save_h_bar_chart_button.show()

    def toggle_line_chart(self):
        self.h_bar_chart_canvas.hide()
        self.save_h_bar_chart_button.hide()
        self.line_chart_canvas.show()
        self.save_line_chart_button.show()

    def save_h_bar_chart(self):
        name = f"h_bar_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')}.png"
        save_path = self.h_bar_chart_canvas.save_fig(name)
        if save_path:
            self.parent.msg_dialog.display_message(f"Figure saved as {save_path}", "Figure saved")

    def save_line_chart(self):
        name = f"line_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')}.png"
        save_path = self.line_chart_canvas.save_fig(name)
        if save_path:
            self.parent.msg_dialog.display_message(f"Figure saved as {save_path}", "Figure saved")


class MyCanvas(FigureCanvasQTAgg):

    def __init__(self, width, height, dpi):
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(width, height)
        self.fig.set_dpi(dpi)
        super().__init__(self.fig)

    def h_bar_chart(self, df_):  # mostly from visualization.py -> horizontal_bar_chart
        # clear axes first
        self.ax.cla()
        # plot horizontal bar chart on subplot (empty df_ is fine)
        x_data = df_.columns  # active failure detectors
        metrics = df_.index  # active metrics
        bar_width = 0.1  # width of a single bar, can be dynamic
        interval = 0.01  # interval within a group of bars

        for i, m in enumerate(reversed(metrics)):
            y_data = df_.loc[m]
            y_range = [i * bar_width + i * interval + p for p in range(len(x_data))]
            self.ax.barh(y=y_range, width=y_data, height=bar_width, label=m)
            for x, y in zip(y_range, y_data):
                x_position = y + 1.8  # manually set
                y_position = x - 0.04  # manually set
                self.ax.text(x_position, y_position, y, ha='center', va='bottom')

        self.ax.set_xticks([i for i in range(0, 110, 10)])  # [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        y_ticks = [((len(metrics) - 1) * bar_width + (len(metrics) - 1) * interval) / 2 + p for p in
                   range(len(x_data))]
        self.ax.set_yticks(y_ticks, x_data)

        self.ax.set_ylabel("Algorithm")
        self.ax.set_xlabel("Score")
        self.ax.set_title("Performance Overview")

        # add legend only if x and y axes both have data
        if not (x_data.empty or metrics.empty):
            handles, labels = self.ax.get_legend_handles_labels()
            # about legend location: https://stackoverflow.com/questions/4700614/how-to-put-the-legend-outside-the-plot
            self.ax.legend(reversed(handles), reversed(labels), loc="upper center",
                           bbox_to_anchor=(0.5, -0.07), ncol=len(metrics))

        # draw on canvas
        self.draw()

    def line_chart(self, df_):  # mostly from visualization.py -> line_chart
        # clear axes first
        self.ax.cla()
        # plot line chart on subplot (empty df_ is fine)
        x_data = df_.index  # active metrics
        failure_detectors = df_.columns  # active failure detectors

        for fd in failure_detectors:
            y_data = df_[fd][x_data]

            self.ax.plot(x_data, y_data, label=fd, marker='o')
            for x, y in zip(x_data, y_data):
                self.ax.text(x, y, y, ha='center', va='bottom')

        self.ax.set_yticks([i for i in range(0, 110, 10)])  # [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

        self.ax.set_xlabel("Metric")
        self.ax.set_ylabel("Score")
        self.ax.set_title("Performance Overview")

        # add legend only if x and y axes both have data
        if not (x_data.empty or failure_detectors.empty):
            self.ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.07), ncol=len(failure_detectors))

        # draw on canvas
        self.draw()

    def save_fig(self, default_name):
        default_path = os.path.join(os.getcwd(), default_name)
        file_path, _ = QFileDialog.getSaveFileName(self, "Save figure", default_path, "PNG files (*.png)")
        if file_path:
            self.fig.savefig(file_path, dpi=120)
        return file_path


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # get user's screen resolution
    U_GEOMETRY = app.desktop().screenGeometry()
    U_WIDTH, U_HEIGHT = U_GEOMETRY.width(), U_GEOMETRY.height()
    app.setStyle("Fusion")
    app.setStyleSheet("QLabel {font-size: 12pt;} QPushButton {font-size: 12pt;}")
    window = MainWindow()
    sys.exit(app.exec_())
