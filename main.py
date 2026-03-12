from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox,
    QSpinBox, QScrollArea
)
import sys
import json
import os


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
    def __init__(self, save_name):
        super().__init__()

        self.save_name = save_name
        self.setWindowTitle("Magic Statues")
        self.setFixedSize(600, 500)

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
            # Mundo 1
            ("Pantanal das Nuvens", 1, "22-42"),
            ("Subúrbio Leste", 1, "25-45"),
            ("Espaço Zen", 1, "28-48"),
            ("Oásis do Céu", 1, "30-50"),
            ("Lago do Sol Norte", 1, "30-50"),
            ("Ilha do Sol", 1, "30-50"),
            ("Duo-la Neve", 1, "30-50"),
            ("Planalto do Sol Nascente", 1, "30-50"),

            # Mundo 2
            ("Pantanal Proibido", 2, "40-60"),
            ("Sakura Dançante", 2, "40-60"),
            ("Floresta Adormecida", 2, "50-70"),
            ("Pradaria Ta-ke", 2, "50-70"),
            ("Vila do Sol", 2, "50-70"),
            ("Areia do Mar Vago", 2, "50-70"),

            # Mundo 3
            ("Lago do Sol Sul", 3, "60-80"),
            ("Caminho dos raivosos", 3, "70-90"),
            ("Campo da Rocha Gelada", 3, "80-100"),
            ("Floresta Yu-feng", 3, "85-105"),
            ("Montanhas Yun-lu", 3, "90-110"),
            ("Caminho do Bambu", 3, "95-115"),
            ("Meilin Nevada", 3, "95-115"),
            ("Terra das Rochas Mágicas", 3, "100-120"),

            # Mundo 4
            ("Abismo da Calmaria", 4, "106-126"),
            ("Bacia do Vale Linglan", 4, "106-126"),
            ("Vale do Demônio", 4, "110-130"),
            ("Terra da Luz Perdida", 4, "115-135"),
            ("Terra das Ilusões", 4, "120-140"),
            ("Terra das Promossas", 4, "125-145"),

            # Mundo 5
            ("Abismo Polar", 5, "130-150")
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

        # carregar estados salvos automaticamente
        self.load_states()

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

        with open(f"{self.save_name}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print(f"Estados salvos em {self.save_name}.json")

    def load_states(self):

        if not os.path.exists(f"{self.save_name}.json"):
            return

        with open(f"{self.save_name}.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in self.items:
            if item.nome in data:
                item.status = data[item.nome]
                item.update_button()

    def center(self):

        screen = QApplication.primaryScreen().geometry()
        size = self.geometry()

        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2

        self.move(x, y)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow('status_statues')
    window.show()

    sys.exit(app.exec())