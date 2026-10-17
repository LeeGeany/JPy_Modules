import datetime
from PySide6.QtCore import QObject, Signal, Slot

class CViewLogViewerWorker(QObject):
    signal_log_to_base = Signal(str)
    signal_clear_to_base = Signal()

    @Slot(str)
    def on_signal_log_write(self, text):

        current_ = datetime.datetime.now().strftime("%H:%M:%S")
        log_ = f"[{current_}] {text}"
        self.signal_log_to_base.emit(log_)

    @Slot()
    def on_signal_log_clear(self):
        self.signal_clear_to_base.emit()