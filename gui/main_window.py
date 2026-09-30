from PySide6 import QtWidgets, QtCore
from src.pkg_manager import PackageManager

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Universal Package Manager (UPM)")
        self.setGeometry(100, 100, 900, 600)
        
        # Инициализация менеджера пакетов
        self.pkg_manager = PackageManager()
        
        # Создание основного виджета и лейаута
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Заголовок
        title_label = QtWidgets.QLabel("Управление пакетами (Pacman, Flatpak, AUR)")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title_label)

        # Кнопка для загрузки списка пакетов
        self.load_button = QtWidgets.QPushButton("Обновить список всех пакетов")
        self.load_button.clicked.connect(self.load_packages_list)
        layout.addWidget(self.load_button)

        # Таблица для отображения результатов
        self.package_table = QtWidgets.QTableWidget()
        self.package_table.setColumnCount(5) # Source, Name, Version, Actions
        self.package_table.setHorizontalHeaderLabels(["Источник", "Имя Пакета", "Версия", "Приложение ID", "Действие"])
        layout.addWidget(self.package_table)

    def load_packages_list(self):
        """Загружает список пакетов из ядра и отображает его в таблице."""
        print("--- Запуск загрузки списка пакетов GUI ---")
        try:
            # Вызов бэкенда для получения данных
            all_packages = self.pkg_manager.get_all_packages()

            # Очистка таблицы перед загрузкой новых данных
            self.package_table.setRowCount(0)
            
            row_count = len(all_packages)
            self.package_table.setRowCount(row_count)

            for i, pkg in enumerate(all_packages):
                # Заполнение ячеек данными из словаря пакета
                source_text = pkg.get('source', 'N/A').upper()
                name_text = pkg.get('name', 'N/A')
                version_text = pkg.get('version', 'N/A')
                app_id = pkg.get('application_id', '')

                self.package_table.setItem(i, 0, QtWidgets.QTableWidgetItem(source_text))
                self.package_table.setItem(i, 1, QtWidgets.QTableWidgetItem(name_text))
                self.package_table.setItem(i, 2, QtWidgets.QTableWidgetItem(version_text))
                self.package_table.setItem(i, 3, QtWidgets.QTableWidgetItem(app_id))

            # Настройка столбцов
            header = self.package_table.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch) # Источник растягивается
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch) # Имя пакета растягивается
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed) 
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch) # App ID растягивается
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.Visible) # Действие

        except Exception as e:
            print(f"Критическая ошибка при загрузке пакетов в GUI: {e}")
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить список пакетов: {e}")

if __name__ == "__main__":
    # Для запуска этого файла нам потребуется запустить QApplication
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())