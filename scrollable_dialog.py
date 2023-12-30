# Copyright 2023 Issao Hanaoka Junior
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

###
### Conversor de arquivos de imagem para WEBP
### Utiliza a biblioteca libwebp-1.3.2-windows-x64 (https://developers.google.com/speed/webp/docs/precompiled?hl=pt-br)
### Publicado inicialmente em 29/12/2023
###

# Importações necessárias para a criação da caixa de diálogo rolável
from PyQt5.QtWidgets import (
    QDialog, QTextEdit, QVBoxLayout, QScrollArea, 
    QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt

# Classe para criar uma caixa de diálogo rolável
class ScrollableDialog(QDialog):
    def __init__(self, title, text, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(640)
        self.setMinimumHeight(480)
        
        # Remove o botão de ajuda contextual da janela de diálogo
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        layout = QVBoxLayout(self)

        text_edit = QTextEdit()
        text_edit.setPlainText(text)
        text_edit.setReadOnly(True)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(text_edit)

        layout.addWidget(scroll_area)      
        
        # Adiciona um botão de fechar à caixa de diálogo
        button_layout = QHBoxLayout()
        button_layout.addStretch() 
         
        close_button = QPushButton("Fechar")
        close_button.clicked.connect(self.close)
        close_button.setMaximumWidth(100)
        
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)        

# Função para exibir a caixa de diálogo rolável
def show_scrollable_dialog(title, text):
    dialog = ScrollableDialog(title, text)
    dialog.exec_()

