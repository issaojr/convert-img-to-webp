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

# Importando as bibliotecas necessárias
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLabel, QLineEdit, QMenu, QAction, QMessageBox, QListWidget, QDialog, QTextEdit, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt

CONST_QUALITY = "80"

# Função para converter imagens para o formato webp
def convert_to_webp(input_file, output_file):
    base_output_file = output_file
    i = 1
    # Verifica se o arquivo de saída já existe e adiciona um sufixo se necessário
    while os.path.exists(output_file):
        output_file = f"{base_output_file.rsplit('.', 1)[0]}({i}).webp"
        i += 1
    try:
        subprocess.run(["libwebp/bin/cwebp.exe", "-q", CONST_QUALITY, input_file, "-o", output_file], check=True)
    except subprocess.CalledProcessError as e:
        return f"A conversão falhou com o seguinte erro: {e.stderr.decode('utf-8')}"
    return "Conversão concluída com sucesso!"

# Função para selecionar arquivos de entrada
def select_input_files():
    files = QFileDialog.getOpenFileNames()[0]
    if not files:
        return    
    input_files.addItems(files)
    convert_button.setEnabled(True)  # Habilita o botão quando um arquivo é selecionado

# Função para selecionar um diretório de entrada
def select_input_directory():
    directory = QFileDialog.getExistingDirectory()
    if directory:
        input_files.addItem(directory)
        convert_button.setEnabled(True)  # Habilita o botão quando um arquivo é selecionado

# Função para remover um arquivo de entrada
def remove_input_file():
    for item in input_files.selectedItems():
        input_files.takeItem(input_files.row(item))
        if input_files.count() == 0:
            convert_button.setEnabled(False)

# Função para selecionar o diretório de saída
def select_output_dir():
    output_dir.setText(QFileDialog.getExistingDirectory())

# Função para converter os arquivos de entrada
def convert():
    input_files_value = [input_files.item(i).text() for i in range(input_files.count())]
    output_dir_value = output_dir.text()
    messagesList = []

    for input_path_value in input_files_value:
        if os.path.isdir(input_path_value):
            for filename in os.listdir(input_path_value):
                if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.tiff'):
                    input_file = os.path.join(input_path_value, filename)
                    output_file = os.path.join(output_dir_value, os.path.splitext(filename)[0] + '.webp')
                    message = convert_to_webp(input_file, output_file)
            if "Conversão concluída com sucesso!" in message:
                messagesList.append(f'Sucesso! Imagem {input_file} convertida!')
            else:
                messagesList.append(f'Erro! Imagem {input_file} falhou!')
        elif os.path.isfile(input_path_value):
            if input_path_value.endswith('.png') or input_path_value.endswith('.jpg') or input_path_value.endswith('.jpeg') or input_path_value.endswith('.tiff'):
                print(os.path.abspath(input_path_value))
                filename = os.path.basename(input_path_value)
                output_file = os.path.join(output_dir_value, os.path.splitext(filename)[0] + '.webp')
                message = convert_to_webp(input_path_value, output_file)
                if "Conversão concluída com sucesso!" in message:
                    messagesList.append(f'Sucesso! Imagem {input_path_value} convertida!')
                else:
                    messagesList.append(f'Erro! Imagem {input_file} falhou!')
    messagesList.append(f'Conversão concluída! Os arquivos convertidos foram salvos em {output_dir_value}')
    show_scrollable_dialog("Conversão Concluída", messagesList)

# Função para exibir informações sobre o desenvolvedor
def show_about():
    QMessageBox.information(None, "Informações sobre o desenvolvedor", 'Desenvolvido por: Issao Hanaoka Junior\nE-mail: issaojr.dev@gmail.com\nVersão: 0.5.0\nData: 28/12/2023')

# Função para exibir a licença de uso
def show_license():
    with open('LICENSE.txt', 'r', encoding='utf-8') as file:
        license_text = file.read()
        
    show_scrollable_dialog('LICENÇA DE SOFTWARE', license_text)

# Função para exibir janelas de diálogo com textos mais longos que precisam de scroll
def show_scrollable_dialog(title, text):
    app = QApplication([])

    dialog = QDialog()
    dialog.setWindowTitle(title)
    dialog_layout = QVBoxLayout(dialog)

    text_edit = QTextEdit()
    text_edit.setPlainText(text)
    text_edit.setReadOnly(True)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(text_edit)

    dialog_layout.addWidget(scroll_area)

    close_button = QPushButton("Fechar")
    close_button.clicked.connect(dialog.close)
    dialog_layout.addWidget(close_button, alignment=Qt.Alignment())

    dialog.setLayout(dialog_layout)
    dialog.setMinimumWidth(640)
    dialog.setMinimumHeight(480)

    dialog.exec_()

# Função para exibir a ajuda
def show_help():
    with open('README.md', 'r', encoding='utf-8') as file:
        ajuda_text = file.read()
    show_scrollable_dialog("Ajuda", ajuda_text)    


# Criação da aplicação e da janela principal
app = QApplication([])
window = QMainWindow()
central_widget = QWidget()
layout = QVBoxLayout()
title = 'Conversor de Imagens para WEBP'

# Criação dos botões e campos de texto
select_directory_button = QPushButton('Selecionar Diretório')
select_directory_button.clicked.connect(select_input_directory)

input_files_label = QLabel('Selecione os diretórios ou arquivos para converter:')
input_files = QListWidget()
input_files_button = QPushButton('Selecionar arquivo(s)')
input_files_button.clicked.connect(select_input_files)

remove_button = QPushButton('Remover selecionado')
remove_button.clicked.connect(remove_input_file)

output_dir_label = QLabel('Selecione o diretório para os arquivos WEBP criados:')
output_dir = QLineEdit()
output_dir_button = QPushButton('Selecionar Diretório')
output_dir_button.clicked.connect(select_output_dir)

convert_button = QPushButton('Converter')
convert_button.clicked.connect(convert)
convert_button.setEnabled(False)  # Desabilita o botão inicialmente

# Criação do botão 'Sair'
exit_button = QPushButton('Sair')
exit_button.clicked.connect(app.quit)  # Conecta o sinal 'clicked' do botão à função 'quit'

# Adicionando os widgets ao layout
layout.addWidget(input_files_label)
layout.addWidget(input_files)
layout.addWidget(remove_button)
layout.addWidget(select_directory_button)
layout.addWidget(input_files_button)
layout.addWidget(output_dir_label)
layout.addWidget(output_dir)
layout.addWidget(output_dir_button)
layout.addWidget(convert_button)
layout.addWidget(exit_button)

# Configuração do widget central e do layout
central_widget.setLayout(layout)
window.setCentralWidget(central_widget)
window.setWindowTitle(title)


# Criação do menu
menu = window.menuBar()
about_menu = QMenu('Sobre', menu)
about_action = QAction('Informações sobre o desenvolvedor', about_menu)
about_action.triggered.connect(show_about)
about_menu.addAction(about_action)
menu.addMenu(about_menu)

license_menu = QMenu('Licença de uso', menu)
license_action = QAction('Ler a licença de uso', license_menu)
license_action.triggered.connect(show_license)
license_menu.addAction(license_action)
menu.addMenu(license_menu)

help_menu = QMenu('Ajuda', menu)
help_action = QAction('Instruções de uso', help_menu)
help_action.triggered.connect(show_help)
help_menu.addAction(help_action)
menu.addMenu(help_menu)

# Exibição da janela
window.show()

# Execução da aplicação
app.exec_()
