#!/usr/bin/env python3
"""
Inicializador da GUI do Drive de Pobre Downloader
"""

import sys
import os

try:
    from DriveDePobre_Downloader import main
    print("Iniciando Drive de Pobre Downloader GUI...")
    main()
except ImportError as e:
    print(f"Erro de importação: {e}")
    print("Certifique-se de que todas as dependências estão instaladas:")
    print("pip install -r requirements.txt")
    input("Pressione Enter para sair...")
except Exception as e:
    print(f"Erro: {e}")
    input("Pressione Enter para sair...")
