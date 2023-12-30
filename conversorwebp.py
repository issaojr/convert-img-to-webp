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
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout,
    QWidget, QHBoxLayout, QListWidget, QLineEdit, QLabel, QMenu, QAction,
    QMessageBox
)
from PyQt5.QtCore import Qt
from scrollable_dialog import show_scrollable_dialog

# Constantes
CONST_QUALITY = "80"
VERSAO = "0.9.1"
DATA_VERSAO = "30/12/2023"

# Função para incluir imagens na lista de arquivos de entrada
def incluir_imagem():
    # Obtemos uma lista de arquivos de imagem do diálogo de seleção de arquivos
    files, _ = QFileDialog.getOpenFileNames(filter="Imagens (*.png *.jpg *.jpeg *.tiff)")
    if not files:
        return  
    # Adicionamos os arquivos à lista de entrada
    input_files.addItems(files)
    # Verificamos a interface gráfica após a inclusão
    verifyAll() 

# Função para remover itens da lista de arquivos de entrada
def remover():
    for item in input_files.selectedItems():
        input_files.takeItem(input_files.row(item))        
    # Verificamos a interface gráfica após a remoção
    verifyAll()

# Função para selecionar o diretório de saída
def select_directory():
    output_dir.setText(QFileDialog.getExistingDirectory())
    # Verificamos a interface gráfica após a seleção do diretório
    verifyAll()

# Função para limpar os campos de entrada
def clearFields():
    input_files.clear()
    output_dir.clear()
    # Verificamos a interface gráfica após a limpeza
    verifyAll()

# Função que realiza todas as verificações
def verifyAll():
    # Verificamos o botão de conversão e o botão de inclusão de imagens
    verifyConvertButton()
    verifyIncluirImagem()
    
# Função para habilitar/desabilitar botão 'Converter'
def verifyConvertButton():
    enable = False
    # Verificamos se há arquivos de entrada e se o diretório de saída está especificado
    if input_files.count() > 0 and output_dir.text().strip():
        enable = True
    convert_button.setEnabled(enable)
 
# Função para habilitar/desabilitar botão 'Incluir imagens'   
def verifyIncluirImagem():
    enable = True
    # Verificamos se há algum arquivo de entrada na lista
    if input_files.count() > 0:
        enable = False
    incluir_imagem_button.setEnabled(enable)
    
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
    
# Função para converter os arquivos de entrada
def convert():
    # Obtém os valores dos arquivos de entrada e do diretório de saída
    input_files_value = [input_files.item(i).text() for i in range(input_files.count())]
    output_dir_value = output_dir.text()
    messagesList = []

    # Itera sobre os arquivos de entrada
    for input_path_value in input_files_value:
        # Verifica se o caminho é um diretório
        if os.path.isdir(input_path_value):
            # Itera sobre os arquivos no diretório
            for filename in os.listdir(input_path_value):
                # Verifica se o arquivo é uma imagem
                if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.tiff'):
                    input_file = os.path.join(input_path_value, filename)
                    output_file = os.path.join(output_dir_value, os.path.splitext(filename)[0] + '.webp')
                    # Converte o arquivo para o formato webp
                    message = convert_to_webp(input_file, output_file)
            # Adiciona mensagens de sucesso ou falha à lista
            if "Conversão concluída com sucesso!" in message:
                messagesList.append(f'Sucesso! Imagem {input_file} convertida!')
            else:
                messagesList.append(f'Erro! Imagem {input_file} falhou!')
        # Verifica se o caminho é um arquivo individual
        elif os.path.isfile(input_path_value):
            # Verifica se o arquivo é uma imagem
            if input_path_value.endswith('.png') or input_path_value.endswith('.jpg') or input_path_value.endswith('.jpeg') or input_path_value.endswith('.tiff'):
                # Converte o arquivo para o formato webp
                filename = os.path.basename(input_path_value)
                output_file = os.path.join(output_dir_value, os.path.splitext(filename)[0] + '.webp')
                message = convert_to_webp(input_path_value, output_file)
                # Adiciona mensagens de sucesso ou falha à lista
                if "Conversão concluída com sucesso!" in message:
                    messagesList.append(f'Sucesso! Imagem {input_path_value} convertida!')
                else:
                    messagesList.append(f'Erro! Imagem {input_file} falhou!')
    
    # Adiciona uma mensagem final à lista com informações sobre a conversão
    messagesList.append(f'Conversão concluída! Os arquivos convertidos foram salvos em {output_dir_value}')
    messagesText = '\n'.join(messagesList)
    clearFields()  # Limpa os campos após a conversão
    show_scrollable_dialog("Conversão Concluída", messagesText)  # Exibe uma janela de diálogo com as mensagens


# Função para exibir a ajuda
def show_help():
    with open('README.md', 'r', encoding='utf-8') as file:
        ajuda_text = file.read()
    show_scrollable_dialog("Ajuda", ajuda_text)  
    
# Função para exibir informações sobre o desenvolvedor
def show_about():
    QMessageBox.information(None, "Informações sobre o desenvolvedor", f'Desenvolvido por: Issao Hanaoka Junior\nE-mail: issaojr.dev@gmail.com\nVersão: {VERSAO}\nData: {DATA_VERSAO}')

# Função para exibir a licença de uso
def show_license():
    with open('LICENSE.txt', 'r', encoding='utf-8') as file:
        license_text = file.read()
    show_scrollable_dialog("Licença de Software", license_text)           

app = QApplication([])

window = QMainWindow()
central_widget = QWidget()
layout = QVBoxLayout()

# Adicionar menu
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

# Primeira linha: Incluir Imagem, Incluir Pasta e Remover
linha1_layout = QHBoxLayout()

coluna1_linha1_layout = QVBoxLayout()
coluna1_linha1_layout.setAlignment(Qt.AlignTop)
input_files_label = QLabel('Selecionar Arquivo(s) ou Pasta(s)')
coluna1_linha1_layout.addWidget(input_files_label)
coluna1_linha1_layout.addSpacing(15) 


incluir_imagem_button = QPushButton('Incluir Imagem')
incluir_imagem_button.clicked.connect(incluir_imagem)
coluna1_linha1_layout.addWidget(incluir_imagem_button)

remover_button = QPushButton('Remover')
remover_button.clicked.connect(remover)
coluna1_linha1_layout.addWidget(remover_button)

limpar_button = QPushButton('Limpar')
limpar_button.clicked.connect(clearFields)
coluna1_linha1_layout.addWidget(limpar_button)

coluna2_linha1_layout = QVBoxLayout()
input_files = QListWidget()
coluna2_linha1_layout.addWidget(input_files)

linha1_layout.addLayout(coluna1_linha1_layout)
linha1_layout.addLayout(coluna2_linha1_layout)

layout.addLayout(linha1_layout)

# Segunda linha: Selecionar Pasta de Diretório e QlineEdit
linha2_layout = QHBoxLayout()

coluna1_linha2_layout = QVBoxLayout()
output_dir_label = QLabel('Selecionar Diretório para Salvar')
coluna1_linha2_layout.addWidget(output_dir_label)

select_directory_button = QPushButton('Selecionar Diretório')
select_directory_button.clicked.connect(select_directory)
coluna1_linha2_layout.addWidget(select_directory_button)

coluna2_linha2_layout = QVBoxLayout()
output_dir = QLineEdit()
coluna2_linha2_layout.addWidget(output_dir)

linha2_layout.addLayout(coluna1_linha2_layout)
linha2_layout.addLayout(coluna2_linha2_layout)

layout.addLayout(linha2_layout)

# Terceira linha: Botões Sair e Converter
linha3_layout = QHBoxLayout()
linha3_layout.addStretch()

exit_button = QPushButton('Sair')
exit_button.clicked.connect(exit)
linha3_layout.addWidget(exit_button)

convert_button = QPushButton('Converter')
convert_button.clicked.connect(convert)
convert_button.setEnabled(False)
linha3_layout.addWidget(convert_button)

layout.addLayout(linha3_layout)

# Configurando as dimensões da janela
window.setFixedSize(800, 450)
window.setWindowTitle('Conversor de Imagens para WebP')
central_widget.setLayout(layout)
window.setCentralWidget(central_widget)

window.show()
app.exec_()

