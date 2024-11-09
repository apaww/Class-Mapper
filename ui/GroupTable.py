from PyQt5.QtCore import Qt, QMetaObject, QCoreApplication
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QHBoxLayout, QSizePolicy, QTableWidgetItem, QCompleter
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import ComboBox as ChooseMeBox, BodyLabel, LineEdit, InfoBarPosition, InfoBar, PushButton, TogglePushButton, MessageBoxBase, SubtitleLabel, PushButton, CaptionLabel, EditableComboBox as ComboBox

from custom.Table import Table
from custom.UniqueNumber import createSequence
from data.Const import GROUPS, DIFFICULTIES
from data.Database import *
from custom.Normalise import normalise


class CreateMessageBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('Создать группу', self)
        self.numberComboBox = ComboBox(self)
        self.nameComboBox = ComboBox(self)
        self.difficultyComboBox = ComboBox(self)
        self.teacherComboBox = ComboBox(self)

        self.numberComboBox.setPlaceholderText('Номер группы')
        suggestion = [createSequence() for _ in range(5)]
        self.numberComboBox.addItems(suggestion)
        self.numberComboBox.setCurrentIndex(-1)
        completer = QCompleter(suggestion, self)
        completer.setCaseSensitivity(0)
        self.numberComboBox.setCompleter(completer)

        self.nameComboBox.setPlaceholderText('Наименование объединения')
        self.nameComboBox.addItems(GROUPS)
        self.nameComboBox.setCurrentIndex(-1)
        completer = QCompleter(GROUPS, self)
        completer.setCaseSensitivity(0)
        self.nameComboBox.setCompleter(completer)

        self.difficultyComboBox.setPlaceholderText('Сложность обучения')
        self.difficultyComboBox.addItems(DIFFICULTIES)
        self.difficultyComboBox.setCurrentIndex(-1)
        completer = QCompleter(DIFFICULTIES, self)
        completer.setCaseSensitivity(0)
        self.difficultyComboBox.setCompleter(completer)

        self.teacherComboBox.setPlaceholderText('ФИО преподователя')
        suggestion = getTeachers()
        self.teacherComboBox.addItems(suggestion)
        self.teacherComboBox.setCurrentIndex(-1)
        completer = QCompleter(suggestion, self)
        completer.setCaseSensitivity(0)
        self.teacherComboBox.setCompleter(completer)

        self.errorLabel = CaptionLabel("Нужно заполнить все поля!")
        self.errorLabel.setTextColor("#cf1010", QColor(255, 28, 32))

        # createButton widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.numberComboBox)
        self.viewLayout.addWidget(self.nameComboBox)
        self.viewLayout.addWidget(self.difficultyComboBox)
        self.viewLayout.addWidget(self.teacherComboBox)
        self.viewLayout.addWidget(self.errorLabel)
        self.errorLabel.hide()

        # change the text of button
        self.cancelButton.setText('Отменить')
        self.yesButton.setText('Создать')

        self.widget.setMinimumWidth(500)


    def validate(self):
        isValid = True
        if self.numberComboBox.currentText() in getNumbers():
            self.errorLabel.setText("Такой номер группы уже существует!")
            isValid = False
        elif not self.nameComboBox.currentText() or not self.difficultyComboBox.currentText() \
            or not self.teacherComboBox.currentText() or not self.numberComboBox.currentText():
            self.errorLabel.setText("Нужно заполнить все поля!")
            isValid = False
        self.errorLabel.setHidden(isValid)
        return isValid


class EditMessageBox(MessageBoxBase):
    def __init__(self, row, parent=None):
        super().__init__(parent)
        self.row = row
        self.group = getGroup(row)
        self.titleLabel = SubtitleLabel('Изменить группу', self)
        self.numberComboBox = ComboBox(self)
        self.nameComboBox = ComboBox(self)
        self.difficultyComboBox = ComboBox(self)
        self.teacherComboBox = ComboBox(self)

        self.numberComboBox.setText('Номер группы')
        suggestion = [createSequence() for _ in range(5)] + [self.group[0]]
        self.numberComboBox.addItems(suggestion)
        self.numberComboBox.setCurrentIndex(len(suggestion) - 1)
        completer = QCompleter(suggestion, self)
        completer.setCaseSensitivity(0)
        self.numberComboBox.setCompleter(completer)

        self.nameComboBox.setPlaceholderText(self.group[1])
        suggestion = GROUPS + [self.group[1]]
        suggestion = normalise(suggestion)
        self.nameComboBox.addItems(suggestion)
        self.nameComboBox.setCurrentIndex(suggestion.index(self.group[1]))
        completer = QCompleter(suggestion, self)
        completer.setCaseSensitivity(0)
        self.nameComboBox.setCompleter(completer)

        self.difficultyComboBox.setPlaceholderText(self.group[2])
        suggestion = DIFFICULTIES + [self.group[2]]
        suggestion = normalise(suggestion)
        self.difficultyComboBox.addItems(suggestion)
        self.difficultyComboBox.setCurrentIndex(suggestion.index(self.group[2]))
        completer = QCompleter(suggestion, self)
        completer.setCaseSensitivity(0)
        self.difficultyComboBox.setCompleter(completer)

        self.teacherComboBox.setPlaceholderText(self.group[3])
        suggestion = normalise(getTeachers())
        self.teacherComboBox.addItems(suggestion + [self.group[3]])
        self.teacherComboBox.setCurrentIndex(suggestion.index(self.group[3]))
        completer = QCompleter(suggestion + [self.group[3]], self)
        completer.setCaseSensitivity(0)
        self.teacherComboBox.setCompleter(completer)

        self.errorLabel = CaptionLabel("Нужно заполнить все поля!")
        self.errorLabel.setTextColor("#cf1010", QColor(255, 28, 32))

        # createButton widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.numberComboBox)
        self.viewLayout.addWidget(self.nameComboBox)
        self.viewLayout.addWidget(self.difficultyComboBox)
        self.viewLayout.addWidget(self.teacherComboBox)
        self.viewLayout.addWidget(self.errorLabel)
        self.errorLabel.hide()

        # change the text of button
        self.cancelButton.setText('Отменить')
        self.yesButton.setText('Применить')

        self.widget.setMinimumWidth(500)


    def validate(self):
        isValid = True
        if self.numberComboBox.currentText() in getNumbers() and self.numberComboBox.currentText() != self.group[0]:
            self.errorLabel.setText("Такой номер группы уже существует!")
            isValid = False
        if not self.difficultyComboBox.currentText() or not self.numberComboBox.currentText()\
            or not self.teacherComboBox.currentText() or not self.nameComboBox.currentText():
            isValid = False
        self.errorLabel.setHidden(isValid)
        return isValid
    

class DeleteMessageBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('Удалить группу(-ы)', self)
        self.textLabel = BodyLabel('Вы уверены, что хотите удалить эту(-и) группу(-ы)?')

        # createButton widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.textLabel)

        # change the text of button
        self.cancelButton.setText('Отменить')
        self.yesButton.setText('Удалить')

        self.widget.setMinimumWidth(500)


class FiltersMessageBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('Фильтры', self)
        self.categoryBox = ChooseMeBox(self)
        self.paramBox = ComboBox(self)

        categories = ['Наименование объединения', 'Уровень обучения', 'ФИО преподователя']
        self.categoryBox.setPlaceholderText('Выберите категорию')
        self.categoryBox.addItems(categories)
        self.categoryBox.setCurrentIndex(0)
        self.categoryBox.currentTextChanged.connect(self.changeCategory)

        self.items = normalise(getGroupNames())
        self.paramBox.setPlaceholderText('Введите фильтр')
        self.paramBox.addItems(self.items)
        self.paramBox.setCurrentIndex(-1)
        completer = QCompleter(self.items)
        completer.setCaseSensitivity(0)
        self.paramBox.setCompleter(completer)

        self.errorLabel = CaptionLabel("Нужно заполнить все поля!")
        self.errorLabel.setTextColor("#cf1010", QColor(255, 28, 32))

        # createButton widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.categoryBox)
        self.viewLayout.addWidget(self.paramBox)
        self.viewLayout.addWidget(self.errorLabel)
        self.errorLabel.hide()

        # change the text of button
        self.cancelButton.setText('Отменить')
        self.yesButton.setText('Применить')

        self.widget.setMinimumWidth(500)


    def validate(self):
        isValid = True
        if not self.paramBox.currentText():
            isValid = False
        self.errorLabel.setHidden(isValid)
        return isValid
    
    
    def changeCategory(self):
        self.items = [getGroupNames(), getDifficulties(), getTeachers()][self.categoryBox.currentIndex()]
        self.items = normalise(self.items)
        self.paramBox.clear()
        self.paramBox.addItems(self.items)
        self.paramBox.setCurrentIndex(-1)
        completer = QCompleter(self.items)
        completer.setCaseSensitivity(0)
        self.paramBox.setCompleter(completer)


class GroupTable(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.buttonLayout = QHBoxLayout()
        self.filterButton = TogglePushButton(icon=FIF.FILTER, text='Фильтры')
        self.createButton = PushButton(icon=FIF.ADD, text='Добавить')
        self.editButton = PushButton(icon=FIF.SETTING, text='Изменить')
        self.deleteButton = PushButton(icon=FIF.REMOVE, text='Удалить')
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.tableWidget = Table(0, self)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QTableWidgetItem()
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.retranslateUi(self)
        self.tableWidget.draw()
        QMetaObject.connectSlotsByName(self)
        self.tableWidget.resizeColumnsToContents()

        self.buttonLayout.addWidget(self.createButton, 5)
        self.buttonLayout.addWidget(self.editButton, 5)
        self.buttonLayout.addWidget(self.deleteButton, 5)
        self.buttonLayout.addWidget(self.filterButton, 1)
        self.vBoxLayout.addWidget(self.tableWidget, 100)
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.setObjectName(text.replace(' ', '-'))

        self.editButton.clicked.connect(self.showEditDialog)
        self.createButton.clicked.connect(self.showCreateDialog)
        self.deleteButton.clicked.connect(self.showDeleteDialog)
        self.filterButton.clicked.connect(self.filtersPressed)
        

    def showCreateDialog(self):
        dialog = CreateMessageBox(self)
        if dialog.exec():
            addGroup(dialog.numberComboBox.currentText(), dialog.nameComboBox.currentText(),
                     dialog.difficultyComboBox.currentText(), dialog.teacherComboBox.currentText())
            self.tableWidget.draw()


    def showEditDialog(self):
        row = self.tableWidget.selectedRow()
        if len(row) > 1:
            self.createErrorInfoBar("Вы можете редактировать только одну строчку за раз!")
            return
        if len(row) == 0:
            self.createErrorInfoBar("Выберите строчку для редактирования!")
            return
        dialog = EditMessageBox(row[0] + 1, self)
        if dialog.exec():
            editGroup(row[0] + 1, dialog.numberComboBox.text(), dialog.nameComboBox.currentText(),
                     dialog.difficultyComboBox.currentText(), dialog.teacherComboBox.currentText())
            self.tableWidget.draw()

    
    def showDeleteDialog(self):
        row = self.tableWidget.selectedRow()
        if len(row) == 0:
            self.createErrorInfoBar("Вы ничего не выбрали!")
            return
        dialog = DeleteMessageBox(self)
        if dialog.exec():
            delGroups(row[0] + 1, row[-1] + 1)
            self.tableWidget.draw()


    def filtersPressed(self):
        if not self.filterButton.isChecked():
            self.filterButton.setChecked(False)
            self.tableWidget.draw()
            return
        self.showFiltersDialog()


    def showFiltersDialog(self):
        dialog = FiltersMessageBox(self)
        if dialog.exec():
            filters = 'WHERE '
            filters = filters + {'Наименование объединения':'name',
                                  'Уровень обучения':'level',
                                    'ФИО преподователя':'teacher'
                                    }.get(dialog.categoryBox.currentText(), 'NEVER HAPPENS 😊')
            filters = filters + f'=\'{dialog.paramBox.currentText()}\' COLLATE NOCASE'
            self.tableWidget.draw(filters=filters)


    def createErrorInfoBar(self, content):
        InfoBar.error(
            title='Ошибка!',
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=2000,    # won't disappear automatically
            parent=self
        )


    def retranslateUi(self, FodeleteButton):
        _translate = QCoreApplication.translate
        FodeleteButton.setWindowTitle(_translate("FodeleteButton", "FodeleteButton"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("FodeleteButton", "Номер группы"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("FodeleteButton", "Наименование объединения"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("FodeleteButton", "Уровень обучения"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("FodeleteButton", "ФИО преподавателя"))