from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox,
    QSpinBox, QScrollArea
)
import sys
import json


class MapItem(QWidget):
    def __init__(self, nome, mundo, level, parent_window=None):
        super().__init__()

        self.nome = nome
        self.status = "Habilitado"
        self.parent_window = parent_window
        self.level_range = level

        layout = QHBoxLayout()

        self.nome_label = QLabel(nome)
        self.mundo_label = QLabel(f"Mundo {mundo}")
        self.level_label = QLabel(f"Lv {level}")

        self.button = QPushButton()
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
        self.setFixedSize(520, 500)

        self.items = []

        self.init_ui()
        self.center()

    def init_ui(self):

        main_layout = QVBoxLayout()

        filter_layout = QHBoxLayout()

        self.status_filter = QComboBox()
        self.status_filter.addItems(["Nenhum", "Habilitado", "Derrotado"])

        self.level_spin = QSpinBox()
        self.level_spin.setRange(0, 160)
        self.level_spin.setPrefix("Lv ")

        self.reset_maps_btn = QPushButton("Resetar Mapas")
        self.save_btn = QPushButton("Salvar Estados")

        self.status_filter.currentTextChanged.connect(self.apply_filter)
        self.level_spin.valueChanged.connect(self.apply_filter)

        self.reset_maps_btn.clicked.connect(self.reset_maps)
        self.save_btn.clicked.connect(self.save_states)

        filter_layout.addWidget(QLabel("Filtro"))
        filter_layout.addWidget(self.status_filter)
        filter_layout.addWidget(self.level_spin)
        filter_layout.addWidget(self.reset_maps_btn)
        filter_layout.addWidget(self.save_btn)

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

            if status == "Nenhum" and level == 0:
                item.setVisible(True)
                continue

            if level == 0:
                if status == "Nenhum":
                    item.setVisible(True)
                else:
                    item.setVisible(item.status == status)
                continue

            min_lv, max_lv = map(int, item.level_range.split("-"))
            level_match = (min_lv <= level <= max_lv)

            if status == "Nenhum":
                item.setVisible(level_match)
            else:
                status_match = (item.status == status)
                item.setVisible(status_match and level_match)

    def reset_maps(self):

        for item in self.items:
            item.status = "Habilitado"
            item.update_button()

        self.apply_filter()

    def save_states(self):

        data = {}

        for item in self.items:
            data[item.nome] = item.status

        with open("map_states.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print("Estados salvos em map_states.json")

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