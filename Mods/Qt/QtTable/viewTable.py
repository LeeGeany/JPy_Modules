
from PySide6.QtWidgets import QWidget, QHBoxLayout, QTableView
from PySide6.QtCore import Signal, QThread, QObject, Slot, QAbstractTableModel, QModelIndex, Qt

from Utils.myUtil import time_stamp

class CTableModel(QAbstractTableModel):
    def __init__(self, _header=None, parent=None):
        super().__init__(parent)
        self._data = []
        self.header = _header or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.header)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None

        if len(self._data) > 0:
            return self._data[index.row()][index.column()]
        else:
            return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header[section]
        return None

    def add_row(self, _row_list):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(_row_list)
        self.endInsertRows()

    def remove_rows(self, idx):
        if 0 <= idx < self.rowCount():
            self.beginRemoveRows(QModelIndex(), idx, idx)
            del self._data[idx]
            self.endRemoveRows()


class CViewTableWorker(QObject):
    def __init__(self, _header=None):
        super().__init__()
        self.table = QTableView()
        self.model = CTableModel(_header)      # 리스트에 주입할 모델 생성
        self.table.setModel(self.model)

    @Slot(list)
    def on_signal_add_list(self, _list : list):
        self.model.add_row(_list)

    @Slot(int)
    def on_signal_remove_list(self, idx: int):
        self.model.remove_rows(idx)

    @Slot(list, dict, object, str)
    def on_signal_add_condition(self, _list: list, _setting : dict, _condition : object, _filename: str = ""):
        ret = _condition(_list)

        if ret:
            current_time = time_stamp()
            self.model.add_row([f"{current_time}",
                                f"{_setting['start_freq']}{_setting['start_freq_res']}",
                                f"{_setting['end_freq']}{_setting['end_freq_res']}",
                                f"{_setting['clt_point']}points",
                                f"{_setting['alarm_freq']}",
                                f"{_setting['clt_threshold']}dB",
                                f"{_setting['save_file_path']}",
                                f"{_filename}"
                                ])

class CViewTable(QWidget):  # QListView를 직접 상속
    signal_add_list     = Signal(list)
    signal_remove_list  = Signal(int)
    signal_add_condition = Signal(list, dict, object, str)

    def __init__(self,
                 _header=None,
                 _clicked_callback = None,
                 parent=None):
        super().__init__(parent)

        # 이벤트 수행 하는 쓰레드
        self.thread = QThread()
        self.worker = CViewTableWorker(_header=_header)
        self.worker.moveToThread(self.thread)
        self.thread.start()
        self.worker.table.clicked.connect(_clicked_callback)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.worker.table)

        # 시그널 연결
        self.signal_add_list.connect(self.worker.on_signal_add_list)
        self.signal_remove_list.connect(self.worker.on_signal_remove_list)
        self.signal_add_condition.connect(self.worker.on_signal_add_condition)

    def add_row(self, _list : list):
        self.signal_add_list.emit(_list)

    def remove_row(self, idx : int):
        self.signal_remove_list.emit(idx)

    def add_rows_with_condition(self, _list : list, _setting : dict, _condition : object, _filename: str):
        self.signal_add_condition.emit(_list, _setting, _condition, _filename)



