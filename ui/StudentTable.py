from PyQt5.QtCore import Qt, QMetaObject, QCoreApplication, QDate
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QHBoxLayout, QSizePolicy, QTableWidgetItem, QCompleter
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import ComboBox as ChooseMeBox, BodyLabel, LineEdit, InfoBarPosition, InfoBar, PushButton, TogglePushButton, MessageBoxBase, SubtitleLabel, PushButton, CaptionLabel, EditableComboBox as ComboBox

from custom.Table import Table
from custom.UniqueNumber import createSequence, createCode
from data.Const import GROUPS, SEX
from data.Database import *
from custom.Normalise import normalise


class CreateMessageBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('Добавить обучающегося', self)
        self.surnameComboBox = ComboBox(self)
        self.nameComboBox = ComboBox(self)
        self.patronymLabel = LineEdit(self)
        self.birthCalendar = LineEdit(self)
        self.sexComboBox = ChooseMeBox(self)
        self.ngroupComboBox = ComboBox(self)
        self.nunionComboBox = ComboBox(self)
        self.codeComboBox = ComboBox(self)
        self.schoolLabel = LineEdit(self)
        self.parentLabel = LineEdit(self)
        self.phoneLabel = LineEdit(self)

        self.surnameComboBox.setPlaceholderText('Фамилия ученика')
        suggestion = getSurnames()
        self.surnameComboBox.addItems(suggestion)
        self.surnameComboBox.setCurrentIndex(-1)
        completer = QCompleter(suggestion, self)
        completer.setCaseSensitivity(0)
        self.surnameComboBox.setCompleter(completer)

        self.nameComboBox.setPlaceholderText('Имя ученика')
        suggestion: list[Any] = getNamesStudents()
        self.nameComboBox.addItems(suggestion)
        self.nameComboBox.setCurrentIndex(-1)
        completer = QCompleter(suggestion, self)
        completer.setCaseSensitivity(0)
        self.nameComboBox.setCompleter(completer)

        self.patronymLabel.setPlaceholderText('Отчество ученика')

        self.birthCalendar.setPlaceholderText('Дата рождения')

        self.sexComboBox.setPlaceholderText('Пол')
        suggestion = SEX
        self.sexComboBox.addItems(suggestion)
        self.sexComboBox.setCurrentIndex(-1)

        self.ngroupComboBox.setPlaceholderText('Номер группы')
        suggestion = getNumbers()
        self.ngroupComboBox.addItems(suggestion)
        self.ngroupComboBox.setCurrentIndex(-1)
        completer = QCompleter(suggestion, self)
        completer.setCaseSensitivity(0)
        self.ngroupComboBox.setCompleter(completer)


        self.nunionComboBox.setPlaceholderText('Объединение')
        suggestion = getGroupNames()
        self.nunionComboBox.addItems(suggestion)
        self.nunionComboBox.setCurrentIndex(-1)
        completer = QCompleter(suggestion, self)
        completer.setCaseSensitivity(0)
        self.nunionComboBox.setCompleter(completer)


        self.codeComboBox.setPlaceholderText('Личный код')
        suggestion = [createCode() for _ in range(5)]
        self.codeComboBox.addItems(suggestion)
        self.codeComboBox.setCurrentIndex(-1)
        completer = QCompleter(suggestion, self)
        completer.setCaseSensitivity(0)
        self.codeComboBox.setCompleter(completer)


        self.schoolLabel.setPlaceholderText('Наименование ОУ')

        self.parentLabel.setPlaceholderText('ФИО родителя')

        self.phoneLabel.setPlaceholderText('Контакт родителя')
        
        self.errorLabel = CaptionLabel("Нужно заполнить все поля!")
        self.errorLabel.setTextColor("#cf1010", QColor(255, 28, 32))

        # createButton widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.surnameComboBox)
        self.viewLayout.addWidget(self.nameComboBox)
        self.viewLayout.addWidget(self.patronymLabel)
        self.viewLayout.addWidget(self.birthCalendar)
        self.viewLayout.addWidget(self.sexComboBox)
        self.viewLayout.addWidget(self.ngroupComboBox)
        self.viewLayout.addWidget(self.nunionComboBox)
        self.viewLayout.addWidget(self.codeComboBox)
        self.viewLayout.addWidget(self.schoolLabel)
        self.viewLayout.addWidget(self.parentLabel)
        self.viewLayout.addWidget(self.phoneLabel)
        self.viewLayout.addWidget(self.errorLabel)
        self.errorLabel.hide()

        # change the text of button
        self.cancelButton.setText('Отменить')
        self.yesButton.setText('Создать')

        self.widget.setMinimumWidth(500)


    def validate(self):
        isValid = True
        if self.codeComboBox.currentText() in getCodes():
            self.errorLabel.setText("Такой личный код уже существует!")
            isValid = False
        elif not self.surnameComboBox.currentText() or not self.nameComboBox.currentText() \
            or not self.patronymLabel.text() or not self.birthCalendar.text() \
            or not self.sexComboBox.currentText() or not self.ngroupComboBox.currentText() \
            or not self.nunionComboBox.currentText() or not self.codeComboBox.currentText() \
            or not self.schoolLabel.text() or not self.parentLabel.text() \
            or not self.phoneLabel.text():
            self.errorLabel.setText("Нужно заполнить все поля!")
            isValid = False
        elif len(self.birthCalendar.text().split('.')) != 3:
            self.errorLabel.setText("Дата должна быть в формате д.м.гггг!")
            isValid = False
        self.errorLabel.setHidden(isValid)
        return isValid


class EditMessageBox(MessageBoxBase):
    def __init__(self, row, parent=None):
        super().__init__(parent)
        self.row = row
        self.student = getStudent(row + 1)
        self.titleLabel = SubtitleLabel('Изменить обучающегося', self)
        self.surnameComboBox = ComboBox(self)
        self.nameComboBox = ComboBox(self)
        self.patronymLabel = LineEdit(self)
        self.birthCalendar = LineEdit(self)
        self.sexComboBox = ChooseMeBox(self)
        self.ngroupComboBox = ComboBox(self)
        self.nunionComboBox = ComboBox(self)
        self.codeComboBox = ComboBox(self)
        self.schoolLabel = LineEdit(self)
        self.parentLabel = LineEdit(self)
        self.phoneLabel = LineEdit(self)

        self.surnameComboBox.setPlaceholderText('Фамилия ученика')
        suggestion = getSurnames() + [self.student[0]]
        suggestion = normalise(suggestion)
        self.surnameComboBox.addItems(suggestion)
        self.surnameComboBox.setCurrentIndex(suggestion.index(self.student[0]))
        completer = QCompleter(suggestion, self)
        completer.setCaseSensitivity(0)
        self.surnameComboBox.setCompleter(completer)

        self.nameComboBox.setPlaceholderText('Имя ученика')
        suggestion = getNamesStudents() + [self.student[1]]
        suggestion = normalise(suggestion)
        self.nameComboBox.addItems(suggestion)
        self.nameComboBox.setCurrentIndex(suggestion.index(self.student[1]))
        completer = QCompleter(suggestion, self)
        completer.setCaseSensitivity(0)
        self.nameComboBox.setCompleter(completer)

        self.patronymLabel.setPlaceholderText('Отчество ученика')
        self.patronymLabel.setText(self.student[2])

        self.birthCalendar.setPlaceholderText('Дата рождения')
        self.birthCalendar.setText(self.student[3])

        self.sexComboBox.setPlaceholderText('Пол')
        suggestion = SEX
        self.sexComboBox.addItems(suggestion)
        self.sexComboBox.setCurrentIndex(SEX.index(self.student[4]))

        self.ngroupComboBox.setPlaceholderText('Номер группы')
        suggestion = getNumbers() + [self.student[5]]
        suggestion = normalise(suggestion)
        self.ngroupComboBox.addItems(suggestion)
        self.ngroupComboBox.setCurrentIndex(suggestion.index(self.student[5]))
        completer = QCompleter(suggestion, self)
        completer.setCaseSensitivity(0)
        self.ngroupComboBox.setCompleter(completer)


        self.nunionComboBox.setPlaceholderText('Объединение')
        suggestion = getGroupNames() + [self.student[6]]
        suggestion = normalise(suggestion)
        self.nunionComboBox.addItems(suggestion)
        self.nunionComboBox.setCurrentIndex(suggestion.index(self.student[6]))
        completer = QCompleter(suggestion, self)
        completer.setCaseSensitivity(0)
        self.nunionComboBox.setCompleter(completer)


        self.codeComboBox.setPlaceholderText('Личный код')
        suggestion = [createCode() for _ in range(5)] + [self.student[7]]
        suggestion = normalise(suggestion)
        self.codeComboBox.addItems(suggestion)
        self.codeComboBox.setCurrentIndex(suggestion.index(self.student[7]))
        completer = QCompleter(suggestion, self)
        completer.setCaseSensitivity(0)
        self.codeComboBox.setCompleter(completer)


        self.schoolLabel.setPlaceholderText('Наименование ОУ')
        self.schoolLabel.setText(self.student[8])

        self.parentLabel.setPlaceholderText('ФИО родителя')
        self.parentLabel.setText(self.student[9])

        self.phoneLabel.setPlaceholderText('Контакт родителя')
        self.phoneLabel.setText(self.student[10])
        
        self.errorLabel = CaptionLabel("Нужно заполнить все поля!")
        self.errorLabel.setTextColor("#cf1010", QColor(255, 28, 32))

        # createButton widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.surnameComboBox)
        self.viewLayout.addWidget(self.nameComboBox)
        self.viewLayout.addWidget(self.patronymLabel)
        self.viewLayout.addWidget(self.birthCalendar)
        self.viewLayout.addWidget(self.sexComboBox)
        self.viewLayout.addWidget(self.ngroupComboBox)
        self.viewLayout.addWidget(self.nunionComboBox)
        self.viewLayout.addWidget(self.codeComboBox)
        self.viewLayout.addWidget(self.schoolLabel)
        self.viewLayout.addWidget(self.parentLabel)
        self.viewLayout.addWidget(self.phoneLabel)
        self.viewLayout.addWidget(self.errorLabel)
        self.errorLabel.hide()

        # change the text of button
        self.cancelButton.setText('Отменить')
        self.yesButton.setText('Применить')

        self.widget.setMinimumWidth(500)


    def validate(self):
        isValid = True
        if self.codeComboBox.currentText() in getCodes() and self.codeComboBox.currentText() != self.student[7]:
            self.errorLabel.setText("Такой личный код уже существует!")
            isValid = False
        elif not self.surnameComboBox.currentText() or not self.nameComboBox.currentText() \
            or not self.patronymLabel.text() or not self.birthCalendar.text() \
            or not self.sexComboBox.currentText() or not self.ngroupComboBox.currentText() \
            or not self.nunionComboBox.currentText() or not self.codeComboBox.currentText() \
            or not self.schoolLabel.text() or not self.parentLabel.text() \
            or not self.phoneLabel.text():
            self.errorLabel.setText("Нужно заполнить все поля!")
            isValid = False
        elif len(self.birthCalendar.text().split('.')) != 3:
            self.errorLabel.setText("Дата должна быть в формате д.м.гггг!")
            isValid = False
        self.errorLabel.setHidden(isValid)
        return isValid
    

class DeleteMessageBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('Удалить обучающегося(-ихся)', self)
        self.textLabel = BodyLabel('Вы уверены, что хотите удалить этого(-их) обучающегося(-ихся)?')

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


class StudentTable(QFrame):
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

        self.tableWidget = Table(1, self)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(11)
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
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.retranslateUi(self)
        self.tableWidget.draw()
        QMetaObject.connectSlotsByName(self)
        self.tableWidget.resizeColumnsToContents()

        self.retranslateUi(self)
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
            addStudent(dialog.surnameComboBox.currentText(),dialog.nameComboBox.currentText(),
                        dialog.patronymLabel.text(), dialog.birthCalendar.text(),
                        dialog.sexComboBox.currentText(), dialog.ngroupComboBox.currentText(),
                        dialog.nunionComboBox.currentText(), dialog.codeComboBox.currentText(),
                        dialog.schoolLabel.text(), dialog.parentLabel.text(),
                        dialog.phoneLabel.text())
            self.tableWidget.draw()


    def showEditDialog(self):
        row = self.tableWidget.selectedRow()
        row = [row[i] for i in range(0, len(row), 3)]
        if len(row) > 1:
            self.createErrorInfoBar("Вы можете редактировать только одну строчку за раз!")
            return
        if len(row) == 0:
            self.createErrorInfoBar("Выберите строчку для редактирования!")
            return
        dialog = EditMessageBox(row[0], self)
        if dialog.exec():
            editStudent(row[0] + 1, dialog.surnameComboBox.currentText(),dialog.nameComboBox.currentText(),
                        dialog.patronymLabel.text(), dialog.birthCalendar.text(),
                        dialog.sexComboBox.currentText(), dialog.ngroupComboBox.currentText(),
                        dialog.nunionComboBox.currentText(), dialog.codeComboBox.currentText(),
                        dialog.schoolLabel.text(), dialog.parentLabel.text(),
                        dialog.phoneLabel.text())
            self.tableWidget.draw()

    
    def showDeleteDialog(self):
        row = self.tableWidget.selectedRow()
        if len(row) == 0:
            self.createErrorInfoBar("Вы ничего не выбрали!")
            return
        dialog = DeleteMessageBox(self)
        if dialog.exec():
            delStudents(row[0] + 1, row[-1] + 1)
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


    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Фамилия"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Имя"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Отчество"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Дата рождения"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Пол"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Номер группы"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "Объединение"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Form", "Личный код"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("Form", "Наименование ОУ"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("Form", "ФИО родителя"))
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText(_translate("Form", "Контакт родителя"))