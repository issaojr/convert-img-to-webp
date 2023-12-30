# Conversor de Imagens WebP

Este é um aplicativo de desktop simples, desenvolvido em Python, que permite converter imagens nos formatos PNG, JPEG e TIFF para o formato WebP.

## Funcionalidades

- Seleção de vários arquivos ou um diretório inteiro para conversão.
- Opção para remover arquivos da lista de entrada.
- Evita a sobrescrita de arquivos existentes adicionando um sufixo ao nome do arquivo.
- Interface amigável com espaçamento adequado entre os itens e alinhamento dos botões à direita.
- Menu com opções 'Sobre', 'Licença de uso' e 'Ajuda'.
- É importante ressaltar que este aplicativo não apaga ou modifica os arquivos originais, mas apenas cria novos arquivos no formato WEBP, e caso já existam arquivos WEBP com o mesmo nome, novos arquivos serão criados com sufixo nomedoarquivo(1).webp. Isto garante que nenhum arquivo será sobrescrito ou apagado por equívoco.

## Como usar

1. Clique em 'Selecionar Diretório' para escolher um diretório inteiro para conversão, ou clique em 'Selecionar arquivo(s)' para escolher arquivos individuais.
2. Se quiser remover algum arquivo da lista de entrada, selecione o arquivo e clique em 'Remover selecionado'.
3. Escolha o diretório de saída clicando em 'Selecionar Diretório' ao lado do campo 'Selecione o diretório de saída:'.
4. Clique em 'Converter' para iniciar a conversão dos arquivos. Você será notificado quando a conversão for concluída.

## Dependências

- Python 3
- PyQt5
- cwebp (libwebp-1.3.2-windows-x64 (https://developers.google.com/speed/webp/docs/precompiled?hl=pt-br - incluído no diretório do projeto)

## Desenvolvedor

Desenvolvido por: Issao Hanaoka Junior
E-mail: issaojr.dev@gmail.com
Versão: 0.9.1
Data: 30/12/2023
