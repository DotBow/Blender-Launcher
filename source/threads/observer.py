from PyQt5.QtCore import QThread, pyqtSignal


class Observer(QThread):
    started = pyqtSignal()
    finished = pyqtSignal()
    count_changed = pyqtSignal('PyQt_PyObject')

    def __init__(self, parent):
        QThread.__init__(self)
        self.parent = parent
        self.processes = []

    def run(self):
        self.started.emit()

        while self.parent:
            for proc in self.processes:
                if proc.poll() is not None:
                    proc.kill()
                    self.processes.remove(proc)
                    proc_count = len(self.processes)

                    if proc_count > 0:
                        self.count_changed.emit(proc_count)
                    else:
                        self.finished.emit()
                        return

            QThread.sleep(1)

    def append_proc(self, proc):
        self.processes.append(proc)
        self.count_changed.emit(len(self.processes))
