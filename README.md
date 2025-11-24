# PDF to Word Converter

Aplicativo desktop profissional para converter arquivos PDF em Word (.docx), com suporte a OCR offline e interface moderna.

## Funcionalidades

*   **Conversão PDF para Word**: Preserva formatação original.
*   **OCR Offline**: Reconhecimento de texto em imagens (requer Tesseract).
*   **Interface Moderna**: Tema escuro/claro, suporte a arrastar e soltar.
*   **Multilíngue**: Português, Inglês e Espanhol.
*   **Conversão em Lote**: Processe múltiplos arquivos de uma vez.

## Requisitos

*   Windows 11 ou superior.
*   Python 3.10+ (para desenvolvimento).
*   **[Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki) (OBRIGATÓRIO para OCR)**:
    *   Baixe e instale a versão para Windows (ex: `tesseract-ocr-w64-setup-v5.x.x.exe`).
    *   Durante a instalação, instale os pacotes de idioma (Portuguese, Spanish).
    *   O programa tentará encontrar o Tesseract automaticamente em `C:\Program Files\Tesseract-OCR`.


## Instalação (Desenvolvimento)

1.  Clone o repositório ou baixe o código.
2.  Crie um ambiente virtual:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4.  Execute o aplicativo:
    ```bash
    python main.py
    ```

## Como Gerar o Executável (.exe)

1.  Certifique-se de ter as dependências instaladas.
2.  Instale o PyInstaller:
    ```bash
    pip install pyinstaller
    ```
3.  Execute o comando de build:
    ```bash
    pyinstaller build_exe.spec
    ```
4.  O executável será gerado na pasta `dist/PDFConverter`.

## Como Criar o Instalador

1.  Baixe e instale o [Inno Setup](https://jrsoftware.org/isdl.php).
2.  Gere o executável primeiro (passo anterior).
3.  Abra o arquivo `installer_script.iss` no Inno Setup Compiler.
4.  Clique em "Compile".
5.  O instalador `PDFConverter_Setup.exe` será gerado na raiz do projeto.

## Estrutura do Projeto

*   `app/`: Código fonte principal.
    *   `core/`: Lógica de negócio (conversão, OCR).
    *   `ui/`: Interface gráfica (PySide6).
    *   `utils/`: Utilitários e internacionalização.
    *   `assets/`: Ícones e recursos.
*   `main.py`: Ponto de entrada.
*   `build_exe.spec`: Configuração do PyInstaller.
