# interface.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QPushButton, QMessageBox, QApplication, QLabel, \
    QCheckBox, QComboBox
from PyQt5.QtCore import QDate
import importlib

import sentinel_hub
importlib.reload(sentinel_hub)

class DateSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Select Satellite Data Options')

        layout = QVBoxLayout()

        # provider label
        layout.addWidget(QLabel('Choose your satellite provider:', self))

        # checkbox for sentinel hub
        self.sentinelhub = QCheckBox('Sentinel Hub', self)
        self.sentinelhub.setChecked(True)
        layout.addWidget(self.sentinelhub)

        # TODO: add more checkboxes for future providers

        self.truecolor = QCheckBox('True Color', self)
        self.truecolor.setChecked(True)
        layout.addWidget(self.truecolor)

        # TODO: decide -> dropdown menu or checkbox
        #combobox = QComboBox()
        #combobox.addItems(['True Color', 'Two', 'Three', 'Four'])
        #layout.addWidget(combobox)

        #file type label
        layout.addWidget(QLabel('Choose your file type:', self))

        #dropdown for file type
        self.file_type_combobox = QComboBox()
        self.file_type_combobox.addItems(['TIFF', 'PNG', 'JPEG'])
        layout.addWidget(self.file_type_combobox)

        # checkbox for download
        self.download = QCheckBox('Download', self)
        self.download.setChecked(True)
        layout.addWidget(self.download)

        # import into qgis -> not working right now
        #self.import_qgis = QCheckBox('Import into QGIS', self)
        #self.import_qgis.setChecked(True)
        #layout.addWidget(self.import_qgis)

        # calendar label
        layout.addWidget(QLabel('Choose your time frame:', self))

        # start date calendar
        layout.addWidget(QLabel('Start date:', self))
        self.start_calendar = QCalendarWidget(self)
        self.start_calendar.setGridVisible(True)
        self.start_calendar.setMaximumDate(QDate.currentDate())
        layout.addWidget(self.start_calendar)

        # end date calendar
        layout.addWidget(QLabel('End date:', self))
        self.end_calendar = QCalendarWidget(self)
        self.end_calendar.setGridVisible(True)
        self.end_calendar.setMaximumDate(QDate.currentDate())
        layout.addWidget(self.end_calendar)

        # button to submit
        submit_btn = QPushButton('Submit', self)
        submit_btn.clicked.connect(self.submit)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    def submit(self):
        # format dates for sentinel hub request
        start_date = self.start_calendar.selectedDate().toString("yyyy-MM-dd")
        end_date = self.end_calendar.selectedDate().toString("yyyy-MM-dd")
        download_checked = self.download.isChecked()
        selected_file_type = self.file_type_combobox.currentText()
        if start_date > end_date:
            QMessageBox.critical(self, 'Error', 'End date should be after start date.')
        else:
            try:
                # call methods from sentinel_hub.py
                #sentinel_hub.import_into_qgis()
                sentinel_hub.true_color_without_clouds(start_date, end_date, download_checked, selected_file_type)
                #sentinel_hub.true_color_with_cloud_mask(start_date, end_date)
                #sentinel_hub.true_color_with_clouds(start_date, end_date)
                QMessageBox.information(self, 'Success', f'Successfully processed data for dates: {start_date} to {end_date}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to process data: {e}')

