from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox,
    QSpinBox, QScrollArea
)
import sys


class MapItem(QWidget):
    def __init__(self, nome, mundo, level, parent_window=None):
        super().__init__()

        self.status = "Habilitado"
        self.parent_window = parent_window
        self.level_range = level

        layout = QHBoxLayout()

        # labels
        self.nome_label = QLabel(nome)
        self.mundo_label = QLabel(f"Mundo {mundo}")
        self.level_label = QLabel(f"Lv {level}")

        # botão
        self.button = QPushButton("Habilitado")
        self.button.clicked.connect(self.toggle_status)

        self.update_button()

        layout.addWidget(self.nome_label)
        layout.addWidget(self.mundo_label)
        layout.addWidget(self.level_label)
        layout.addStretch()
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                border: 1px solid #444;
                padding: 6px;
                border-radius: 6px;
            }
        """)

    def toggle_status(self):

        if self.status == "Habilitado":
            self.status = "Derrotado"
        else:
            self.status = "Habilitado"

        self.update_button()

        # reaplicar filtro quando mudar status
        if self.parent_window:
            self.parent_window.apply_filter()

    def update_button(self):

        if self.status == "Derrotado":
            self.button.setText("Derrotado")
            self.button.setStyleSheet("""
                background-color: red;
                color: white;
                font-weight: bold;
            """)
        else:
            self.button.setText("Habilitado")
            self.button.setStyleSheet("""
                background-color: green;
                color: white;
                font-weight: bold;
            """)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mapas")
        self.setFixedSize(500, 500)

        self.items = []

        self.init_ui()
        self.center()

    def init_ui(self):

        main_layout = QVBoxLayout()

        # filtros
        filter_layout = QHBoxLayout()

        self.status_filter = QComboBox()
        self.status_filter.addItems(["Derrotado", "Habilitado"])

        self.level_spin = QSpinBox()
        self.level_spin.setRange(1, 160)

        self.status_filter.currentTextChanged.connect(self.apply_filter)
        self.level_spin.valueChanged.connect(self.apply_filter)

        filter_layout.addWidget(QLabel("Filtro"))
        filter_layout.addWidget(self.status_filter)
        filter_layout.addWidget(QLabel("Lv"))
        filter_layout.addWidget(self.level_spin)

        # scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()

        mapas = [
            ("Mapa Goblin", 1, "1-20"),
            ("Floresta Sombria", 1, "21-40"),
            ("Castelo Antigo", 2, "41-60"),
            ("Caverna de Gelo", 3, "61-80"),
            ("Ruínas Perdidas", 4, "81-100"),
            ("Templo Sagrado", 5, "101-120"),
            ("Inferno Final", 7, "121-160")
        ]

        for nome, mundo, level in mapas:
            item = MapItem(nome, mundo, level, self)
            self.items.append(item)
            scroll_layout.addWidget(item)

        scroll_layout.addStretch()

        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)

        main_layout.addLayout(filter_layout)
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)

    def apply_filter(self):

        status = self.status_filter.currentText()
        level = self.level_spin.value()

        for item in self.items:

            status_match = (item.status == status)

            min_lv, max_lv = map(int, item.level_range.split("-"))
            level_match = (min_lv <= level <= max_lv)

            item.setVisible(status_match and level_match)

    def center(self):

        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()

        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2

        self.move(x, y)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())