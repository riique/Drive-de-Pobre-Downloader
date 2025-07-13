# Drive de Pobre Downloader

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![Requests](https://img.shields.io/badge/Library-Requests-orange.svg)
![BeautifulSoup](https://img.shields.io/badge/Web%20Scraping-BeautifulSoup-lightgrey.svg)
![Selenium](https://img.shields.io/badge/Automation-Selenium-red.svg)
![Tqdm](https://img.shields.io/badge/Progress-Tqdm-purple.svg)

## 🚀 Visão Geral

O **Drive de Pobre Downloader** é uma aplicação desktop intuitiva, desenvolvida em Python com `Tkinter`, projetada para simplificar o download de arquivos e pastas hospedados na plataforma de compartilhamento de arquivos `drivedepobre.com`. Com uma interface gráfica amigável, o aplicativo permite escanear URLs de pastas, visualizar o conteúdo de forma hierárquica e selecionar múltiplos itens para download, incluindo o conteúdo de subpastas.

Ideal para quem busca uma ferramenta eficiente para gerenciar e baixar grandes volumes de dados de forma organizada.

## ✨ Funcionalidades

*   **Interface Gráfica Intuitiva (GUI):** Desenvolvida com `Tkinter` para uma experiência de usuário simplificada.
*   **Escaneamento de Pastas:** Insira uma URL de pasta (`drivedepobre.com/pasta/ID`) para escanear e listar todos os arquivos e subpastas.
*   **Visualização Hierárquica:** Exibe o conteúdo da pasta em uma estrutura de árvore (`Treeview`), facilitando a navegação e seleção.
*   **Seleção Múltipla:** Permite selecionar arquivos e pastas individualmente ou em massa para download.
*   **Download Recursivo:** Baixa automaticamente todos os arquivos dentro das pastas selecionadas, mantendo a estrutura original.
*   **Barra de Progresso:** Acompanhe o status do download com uma barra de progresso detalhada.
*   **Gerenciamento de Destino:** Escolha facilmente a pasta de destino para seus downloads.
*   **Verificação de Tipo de Item:** Heurística inteligente para diferenciar arquivos e pastas durante o escaneamento.

## 📋 Requisitos

Para executar o **Drive de Pobre Downloader**, você precisará ter o Python instalado em seu sistema. As dependências adicionais são gerenciadas via `pip`.

*   **Python 3.x**
*   **Bibliotecas Python:**
    *   `requests`
    *   `beautifulsoup4`
    *   `selenium`
    *   `tqdm`

## 📦 Instalação

Siga os passos abaixo para configurar e executar o projeto em sua máquina local:

1.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/riique/DriveDePobre_Downloader.git
    cd DriveDePobre_Downloader
    ```
    *(Substitua `https://github.com/riique/DriveDePobre_Downloader.git` pelo link real do seu repositório)*

2.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Como Usar

1.  **Inicie a Aplicação:**
    *   **Windows:** Execute o arquivo `Iniciar.bat`
    *   **Outros SOs (Linux/macOS):** Execute o script `Iniciar.py`
        ```bash
        python Iniciar.py
        ```

2.  **Insira a URL da Pasta:**
    *   Na interface gráfica, cole a URL da pasta do `drivedepobre.com` no campo "URL da Pasta". O formato esperado é `https://drivedepobre.com/pasta/ID`.

3.  **Escanear Pasta:**
    *   Clique no botão "Escanear Pasta". O aplicativo listará todos os arquivos e subpastas encontrados na URL fornecida.

4.  **Selecione os Arquivos para Download:**
    *   Use a visualização em árvore para navegar e selecionar os arquivos e pastas que deseja baixar. Você pode usar "Selecionar Todos" ou "Desmarcar Todos" para facilitar.
    *   Um clique duplo em um item alterna sua seleção.

5.  **Escolha a Pasta de Destino:**
    *   Clique no botão "..." ao lado do campo "Pasta:" para escolher onde os arquivos serão salvos. Por padrão, eles serão salvos em uma pasta `downloads` no diretório do projeto.

6.  **Inicie o Download:**
    *   Clique no botão "Baixar Selecionados" para iniciar o processo de download. A barra de progresso indicará o andamento.

## 📂 Estrutura do Projeto

```
.
├── DriveDePobre_Downloader.py  # Lógica principal da aplicação GUI e download
├── Iniciar.py                  # Script de inicialização da aplicação
├── Iniciar.bat                 # Script de inicialização para Windows
├── requirements.txt            # Lista de dependências do Python
└── README.md                   # README
```

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.