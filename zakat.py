import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QCheckBox, QPushButton, QMessageBox, QLineEdit, QScrollArea, QHBoxLayout
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import Qt

# Dictionnaire contenant les différents types de nourriture pour Zakat El Fitr avec leurs quantités en kg
nourriture_zakat = {
    "الدقيق": 2,
    "الفرينة": 1.4,
    "العدس": 2.1,
    "اللوبيا": 2.06,
    "الجلبانة المكسرة": 2.224,
    "القمح": 2.04,
    "الزبيب": 1.64,
    "الكسكس": 1.8,
    "المحمصة": 2,
    "التمر": 1.8,
    "الحمص": 2,
    "الأرز": 2.3
}

# Dictionnaire contenant les prix pour chaque nourriture
prix_nourriture = {
    "الدقيق": 45,
    "الفرينة": 65,
    "العدس": 200,
    "اللوبيا": 230,
    "الجلبانة المكسرة": 280,
    "القمح": 50,
    "الزبيب": 1000,
    "الكسكس": 140,
    "المحمصة": 100,
    "التمر": 700,
    "الحمص": 320,
    "الأرز": 300
}

class ZakatElFitrCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('حاسبة زكاة الفطر')
        self.setWindowIcon(QIcon('img/icon.png'))  
        self.setStyleSheet("background-color: #f0f0f0;")  
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        header_label = QLabel()
        header_pixmap = QPixmap("img/zakat_fitr.jpg")
        header_pixmap = header_pixmap.scaledToWidth(500)  
        header_label.setPixmap(header_pixmap)
        header_label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(header_label)

        label_intro = QLabel("قد ثبت عن رسول الله ﷺ أنه فرض زكاة الفطر على المسلمين صاعاً من تمر أو صاعاً من شعير، وأمر بها أن تؤدى قبل خروج الناس إلى الصلاة، أعني صلاة العيد.")
        label_intro.setStyleSheet("font-family: 'DIN Next LT Arabic'; font-size: 16pt; color: #333;")  
        label_intro.setAlignment(Qt.AlignCenter)
        vbox.addWidget(label_intro)

        label_personnes = QLabel("إختر عدد الأشخاص:")
        label_personnes.setStyleSheet("font-family: 'DIN Next LT Arabic'; font-size: 14pt; color: #333;") 
        vbox.addWidget(label_personnes)

        self.nombre_personnes_input = QLineEdit()
        self.nombre_personnes_input.setStyleSheet("border: 1px solid #ccc; border-radius: 5px; padding: 8px;")
        self.nombre_personnes_input.setAlignment(Qt.AlignCenter)
        self.nombre_personnes_input.setFont(QFont("DIN Next LT Arabic", 14)) 
        vbox.addWidget(self.nombre_personnes_input)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        self.checkbox_vars = []
        for nourriture in nourriture_zakat:
            hbox = QHBoxLayout()

            label_icon = QLabel()
            pixmap = QPixmap(f"img/{list(nourriture_zakat.keys()).index(nourriture) + 1}.jpg")
            pixmap = pixmap.scaledToWidth(50) 
            label_icon.setPixmap(pixmap)
            hbox.addWidget(label_icon)

            checkbox = QCheckBox(nourriture, self)
            checkbox.setStyleSheet("QCheckBox { color: #333; }")
            checkbox.setFont(QFont("DIN Next LT Arabic", 12)) 
            hbox.addWidget(checkbox)
            hbox.setAlignment(Qt.AlignCenter) 
            scroll_layout.addLayout(hbox)

            self.checkbox_vars.append(checkbox)

        scroll_widget.setLayout(scroll_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        vbox.addWidget(scroll_area)

        self.calculate_button = QPushButton('حساب زكاة الفطر', self)
        self.calculate_button.setStyleSheet("QPushButton { color: #fff; background-color: #007bff; border: none; border-radius: 5px; padding: 10px; }"
                                             "QPushButton:hover { background-color: #0056b3; }")
        self.calculate_button.clicked.connect(self.calculer_zakat)
        self.calculate_button.setFont(QFont("DIN Next LT Arabic", 12)) 
        vbox.addWidget(self.calculate_button)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-family: 'DIN Next LT Arabic'; font-size: 14pt; color: #333;") 
        vbox.addWidget(self.result_label)

        self.setLayout(vbox)
        self.show()

    def calculer_zakat(self):
        try:
            nombre_personnes = int(self.nombre_personnes_input.text())
            if nombre_personnes <= 0:
                QMessageBox.critical(self, "خطأ", "يجب أن يكون عدد الأشخاص أكبر من الصفر.")
                return

            types_nourriture = [nourriture for nourriture, checkbox in zip(nourriture_zakat.keys(), self.checkbox_vars) if checkbox.isChecked()]
            total_nourriture = len(types_nourriture)

            total_quantite = {}
            total_prix = 0
            if total_nourriture == 1:
                nourriture = types_nourriture[0]
                total_quantite[nourriture] = nourriture_zakat[nourriture] * nombre_personnes
                total_prix += prix_nourriture[nourriture] * total_quantite[nourriture]
            else:
                quantite_par_nourriture = nombre_personnes // total_nourriture
                reste_personnes = nombre_personnes % total_nourriture

                for nourriture in types_nourriture:
                    quantite = quantite_par_nourriture
                    if reste_personnes > 0:
                        quantite += 1
                        reste_personnes -= 1
                    total_quantite[nourriture] = nourriture_zakat[nourriture] * quantite
                    total_prix += prix_nourriture[nourriture] * total_quantite[nourriture]

            result_text = "زكاة الفطر لـ {} شخص :\n".format(nombre_personnes)
            for nourriture, quantite in total_quantite.items():
                result_text += "{:.3f} كغ من {} بتكلفة {:.3f} دينار جزائري /كغ\n".format(quantite, nourriture, prix_nourriture[nourriture])
            result_text += "\n  التكلفة الإجمالية: {:.3f} دينار جزائري".format(total_prix)
            self.result_label.setText(result_text)

        except ValueError:
            QMessageBox.critical(self, "خطأ", "الرجاء إدخال عدد صحيح لعدد الأشخاص.")
        except ZeroDivisionError:
            QMessageBox.critical(self, "خطأ", "الرجاء إختيار نوع الطعام على الأقل نوع واحد")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ZakatElFitrCalculator()
    sys.exit(app.exec_())
