import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import requests
import os
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import webbrowser


class DriveDePobreGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Drive de Pobre Downloader")
        self.root.geometry("800x600")
        
        # Variáveis
        self.files_data = []
        self.selected_files = {}
        self.download_folder = "downloads"
        self.folder_structure = {}  # Para armazenar estrutura de pastas
        self.tree_items = {}  # Mapear IDs para itens da árvore
        
        # Configurar sessão
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
        })
        
        self.create_widgets()
        self.create_download_folder()
    
    def create_download_folder(self):
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
    
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Drive de Pobre Downloader", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de entrada
        input_frame = ttk.LabelFrame(main_frame, text="URL da Pasta", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Campo de URL
        ttk.Label(input_frame, text="URL:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(input_frame, textvariable=self.url_var, width=50)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # Botão de scan
        self.scan_button = ttk.Button(input_frame, text="Escanear Pasta", 
                                     command=self.scan_folder)
        self.scan_button.grid(row=0, column=2)
        
        # Frame de arquivos
        files_frame = ttk.LabelFrame(main_frame, text="Arquivos Encontrados", padding="10")
        files_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        files_frame.columnconfigure(0, weight=1)
        files_frame.rowconfigure(0, weight=1)
        
        # Treeview para arquivos (com árvore hierárquica)
        columns = ("select", "status")
        self.tree = ttk.Treeview(files_frame, columns=columns, show="tree headings", height=15)
        
        # Configurar colunas
        self.tree.heading("select", text="Baixar")
        self.tree.heading("status", text="Status")
        
        self.tree.column("select", width=60, anchor=tk.CENTER)
        self.tree.column("status", width=150, anchor=tk.CENTER)
        
        # Scrollbar para treeview
        scrollbar = ttk.Scrollbar(files_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind para clique duplo
        self.tree.bind("<Double-1>", self.toggle_selection)
        
        # Frame de controles
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Botões de seleção
        ttk.Button(control_frame, text="Selecionar Todos", 
                  command=self.select_all).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(control_frame, text="Desmarcar Todos", 
                  command=self.deselect_all).grid(row=0, column=1, padx=(0, 5))
        
        # Botões de expansão
        ttk.Button(control_frame, text="Expandir Tudo", 
                  command=self.expand_all).grid(row=0, column=2, padx=(10, 5))
        ttk.Button(control_frame, text="Colapsar Tudo", 
                  command=self.collapse_all).grid(row=0, column=3, padx=(0, 5))
        
        # Botão de download
        self.download_button = ttk.Button(control_frame, text="Baixar Selecionados", 
                                         command=self.start_download, state="disabled")
        self.download_button.grid(row=0, column=4, padx=(20, 0))
        
        # Pasta de destino
        ttk.Label(control_frame, text="Pasta:").grid(row=0, column=5, padx=(20, 5))
        self.folder_var = tk.StringVar(value=self.download_folder)
        folder_entry = ttk.Entry(control_frame, textvariable=self.folder_var, width=20)
        folder_entry.grid(row=0, column=6, padx=(0, 5))
        ttk.Button(control_frame, text="...", width=3,
                  command=self.choose_folder).grid(row=0, column=7)
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                           maximum=100)
        self.progress_bar.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # Label de status
        self.status_var = tk.StringVar(value="Pronto")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=5, column=0, columnspan=3)

        # Créditos
        credit_frame = ttk.Frame(main_frame)
        credit_frame.grid(row=6, column=0, columnspan=3, pady=(10, 0))

        credit_label = ttk.Label(credit_frame, text="Criado por")
        credit_label.grid(row=0, column=0, sticky=tk.W)
        
        riique_link = ttk.Label(credit_frame, text="@riiquestudies", foreground="blue", cursor="hand2")
        riique_link.grid(row=0, column=1, sticky=tk.W)
        riique_link.bind("<Button-1>", lambda e: self.open_link("https://x.com/riiquestudies"))

    def open_link(self, url):
        webbrowser.open_new(url)
    
    def scan_folder(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Erro", "Por favor, insira uma URL válida")
            return
        
        # Extrair ID da pasta
        try:
            if "/pasta/" in url:
                pasta_id = url.split("/pasta/")[-1].split("/")[0]
            else:
                messagebox.showerror("Erro", "URL inválida. Use o formato: https://drivedepobre.com/pasta/ID")
                return
        except:
            messagebox.showerror("Erro", "Não foi possível extrair o ID da pasta")
            return
        
        # Executar scan em thread separada
        self.scan_button.config(state="disabled")
        self.download_button.config(state="disabled")
        self.status_var.set("Escaneando pasta...")
        self.progress_var.set(0)
        
        thread = threading.Thread(target=self._scan_folder_thread, args=(pasta_id,))
        thread.daemon = True
        thread.start()
    
    def _scan_folder_thread(self, pasta_id):
        try:
            self.files_data = []
            self.folder_structure = {}
            self.tree_items = {}
            
            # Escanear pasta recursivamente com limite de profundidade
            self._scan_folder_recursive(pasta_id, "", max_depth=3)
            
            # Atualizar interface na thread principal
            self.root.after(0, self._build_tree_structure)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro ao escanear pasta: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.scan_button.config(state="normal"))
            self.root.after(0, lambda: self.progress_var.set(0))
    
    def _scan_folder_recursive(self, pasta_id, path_prefix, max_depth=5):
        """Escaneia uma pasta recursivamente com limite de profundidade"""
        if max_depth <= 0:
            print(f"Limite de profundidade atingido para pasta: {path_prefix}")
            return
            
        offset = 0
        limit = 50
        items_found = 0
        
        while True:
            url = f"https://api.drivedepobre.com/listFolder?id={pasta_id}&offset={offset}&limit={limit}"
            
            try:
                response = self.session.get(url, timeout=10)
                
                if response.status_code != 200:
                    print(f"Erro HTTP {response.status_code} para pasta {pasta_id}")
                    break
                
                items = response.json()
                if not items or len(items) == 0:
                    break
                
                items_found += len(items)
                current_path = path_prefix or 'raiz'
                print(f"Processando {len(items)} itens em {current_path}")
                
                # Atualizar status na interface
                self.root.after(0, lambda: self.status_var.set(f"Escaneando: {current_path} ({len(self.files_data)} itens encontrados)"))
                
                for item in items:
                    item_id = item.get('id')
                    item_name = item.get('name', 'Sem nome')
                    item_size = item.get('size', 'Desconhecido')
                    
                    if not item_id:
                        continue
                    
                    full_path = f"{path_prefix}/{item_name}" if path_prefix else item_name
                    
                    # Usar heurística mais simples para detectar pastas
                    # Se não tem extensão ou tamanho é "Desconhecido", provavelmente é pasta
                    is_likely_folder = (
                        '.' not in item_name or 
                        item_size == 'Desconhecido' or 
                        item_size == '' or
                        item_size is None
                    )
                    
                    if is_likely_folder:
                        # Verificar se realmente é pasta fazendo uma requisição rápida
                        is_folder = self._quick_folder_check(item_id)
                        
                        if is_folder:
                            # É uma pasta
                            folder_data = {
                                'id': item_id,
                                'name': f"📁 {full_path}",
                                'size': 'Pasta',
                                'url': f"https://drivedepobre.com/pasta/{item_id}",
                                'type': 'folder',
                                'path': full_path,
                                'selected': False,
                                'status': 'Pronto'
                            }
                            self.files_data.append(folder_data)
                            
                            # Escanear conteúdo da pasta recursivamente com profundidade reduzida
                            try:
                                self._scan_folder_recursive(item_id, full_path, max_depth - 1)
                            except Exception as e:
                                print(f"Erro ao escanear subpasta {item_name}: {e}")
                        else:
                            # É um arquivo mesmo sem extensão
                            file_data = {
                                'id': item_id,
                                'name': f"📄 {full_path}",
                                'size': item_size,
                                'url': f"https://drivedepobre.com/arquivo/{item_id}",
                                'type': 'file',
                                'path': full_path,
                                'selected': False,
                                'status': 'Pronto'
                            }
                            self.files_data.append(file_data)
                    else:
                        # Claramente é um arquivo (tem extensão)
                        file_data = {
                            'id': item_id,
                            'name': f"📄 {full_path}",
                            'size': item_size,
                            'url': f"https://drivedepobre.com/arquivo/{item_id}",
                            'type': 'file',
                            'path': full_path,
                            'selected': False,
                            'status': 'Pronto'
                        }
                        self.files_data.append(file_data)
                
                offset += limit
                
                # Limite de segurança para evitar loop infinito
                if items_found > 1000:
                    print(f"Limite de 1000 itens atingido para pasta {path_prefix}")
                    break
                    
                time.sleep(0.3)  # Pausa maior entre requisições
                
            except Exception as e:
                print(f"Erro ao processar pasta {pasta_id}: {e}")
                break
    
    def _quick_folder_check(self, item_id):
        """Verificação rápida se um item é uma pasta"""
        try:
            url = f"https://api.drivedepobre.com/listFolder?id={item_id}&offset=0&limit=1"
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return isinstance(data, list)
                except:
                    return False
            else:
                return False
        except:
            return False
    
    def _build_tree_structure(self):
        """Constrói a estrutura hierárquica da árvore"""
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.tree_items = {}
        
        # Organizar dados por estrutura de pastas
        root_items = []
        folder_contents = {}
        
        for file_data in self.files_data:
            path_parts = file_data['path'].split('/')
            
            if len(path_parts) == 1:
                # Item na raiz
                root_items.append(file_data)
            else:
                # Item dentro de pasta
                parent_path = '/'.join(path_parts[:-1])
                if parent_path not in folder_contents:
                    folder_contents[parent_path] = []
                folder_contents[parent_path].append(file_data)
        
        # Construir árvore recursivamente
        self._build_tree_recursive("", root_items, folder_contents)
        
        self.download_button.config(state="normal" if self.files_data else "disabled")
        
        # Contar arquivos e pastas
        files_count = len([f for f in self.files_data if f['type'] == 'file'])
        folders_count = len([f for f in self.files_data if f['type'] == 'folder'])
        
        status_text = f"{files_count} arquivos"
        if folders_count > 0:
            status_text += f" e {folders_count} pastas"
        status_text += " encontrados"
        
        self.status_var.set(status_text)
    
    def _build_tree_recursive(self, parent_id, items, folder_contents):
        """Constrói a árvore recursivamente"""
        for file_data in items:
            select_text = "☑" if file_data['selected'] else "☐"
            
            # Preparar nome para exibição com ícone
            if file_data['type'] == 'folder':
                display_name = f"📁 {file_data['name'].replace('📁 ', '')}"
            else:
                display_name = f"📄 {file_data['name'].replace('📄 ', '')}"
            
            # Inserir item na árvore
            item_id = self.tree.insert(
                parent_id, 
                "end",
                text=display_name,
                values=(select_text, file_data['status']),
                open=False  # Pastas começam fechadas
            )
            
            # Mapear ID do arquivo para item da árvore
            self.tree_items[file_data['id']] = {
                'tree_item': item_id,
                'data': file_data
            }
            
            # Se é uma pasta, adicionar seus filhos
            if file_data['type'] == 'folder' and file_data['path'] in folder_contents:
                children = folder_contents[file_data['path']]
                self._build_tree_recursive(item_id, children, folder_contents)
    
    def toggle_selection(self, event):
        if not self.tree.selection():
            return
            
        tree_item = self.tree.selection()[0]
        
        # Encontrar dados do arquivo pelo item da árvore
        file_data = None
        for item_info in self.tree_items.values():
            if item_info['tree_item'] == tree_item:
                file_data = item_info['data']
                break
        
        if not file_data:
            return
        
        # Alternar seleção
        file_data['selected'] = not file_data['selected']
        selected = file_data['selected']
        
        # Se é uma pasta, selecionar/desselecionar todos os arquivos dentro dela
        if file_data['type'] == 'folder':
            folder_path = file_data['path']
            self._select_folder_contents(folder_path, selected)
        
        # Atualizar display de todos os itens afetados
        self._update_tree_selection_display()
    
    def _select_folder_contents(self, folder_path, selected):
        """Seleciona/deseleciona todos os arquivos dentro de uma pasta"""
        for file_data in self.files_data:
            if file_data['path'].startswith(folder_path + "/") or file_data['path'] == folder_path:
                file_data['selected'] = selected
    
    def _update_tree_selection_display(self):
        """Atualiza o display de seleção de todos os itens na árvore"""
        for file_data in self.files_data:
            if file_data['id'] in self.tree_items:
                tree_item = self.tree_items[file_data['id']]['tree_item']
                select_text = "☑" if file_data['selected'] else "☐"
                
                # Atualizar valores do item
                current_values = list(self.tree.item(tree_item, "values"))
                current_values[0] = select_text
                self.tree.item(tree_item, values=current_values)
    
    def select_all(self):
        for file_data in self.files_data:
            file_data['selected'] = True
        self._update_tree_selection_display()
    
    def deselect_all(self):
        for file_data in self.files_data:
            file_data['selected'] = False
        self._update_tree_selection_display()
    
    def expand_all(self):
        """Expande todas as pastas na árvore"""
        def expand_item(item):
            self.tree.item(item, open=True)
            for child in self.tree.get_children(item):
                expand_item(child)
        
        for item in self.tree.get_children():
            expand_item(item)
    
    def collapse_all(self):
        """Colapsa todas as pastas na árvore"""
        def collapse_item(item):
            self.tree.item(item, open=False)
            for child in self.tree.get_children(item):
                collapse_item(child)
        
        for item in self.tree.get_children():
            collapse_item(item)
    
    def choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_folder)
        if folder:
            self.folder_var.set(folder)
            self.download_folder = folder
    
    def start_download(self):
        selected_files = [f for f in self.files_data if f['selected']]
        if not selected_files:
            messagebox.showwarning("Aviso", "Nenhum arquivo selecionado")
            return
        
        self.download_folder = self.folder_var.get()
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
        
        # Iniciar download em thread separada
        self.download_button.config(state="disabled")
        thread = threading.Thread(target=self._download_thread, args=(selected_files,))
        thread.daemon = True
        thread.start()
    
    def _download_thread(self, selected_files):
        # Filtrar apenas arquivos (não pastas) para download
        files_to_download = [f for f in selected_files if f['type'] == 'file']
        total_files = len(files_to_download)
        successful = 0
        failed = 0
        
        for i, file_data in enumerate(files_to_download):
            try:
                # Atualizar status
                self.root.after(0, lambda f=file_data: self._update_file_status(f, "Baixando..."))
                self.root.after(0, lambda: self.status_var.set(f"Baixando {i+1}/{total_files}: {file_data['name']}"))
                self.root.after(0, lambda: self.progress_var.set((i / total_files) * 100))
                
                # Baixar arquivo
                if self._download_file(file_data):
                    successful += 1
                    self.root.after(0, lambda f=file_data: self._update_file_status(f, "Concluído"))
                else:
                    failed += 1
                    self.root.after(0, lambda f=file_data: self._update_file_status(f, "Erro"))
                
                time.sleep(0.5)  # Pausa entre downloads
                
            except Exception as e:
                failed += 1
                self.root.after(0, lambda f=file_data: self._update_file_status(f, f"Erro: {str(e)[:20]}"))
        
        # Finalizar
        self.root.after(0, lambda: self.progress_var.set(100))
        self.root.after(0, lambda: self.status_var.set(f"Concluído! {successful} sucessos, {failed} falhas"))
        self.root.after(0, lambda: self.download_button.config(state="normal"))
    
    def _update_file_status(self, file_data, status):
        """Atualiza o status de um arquivo na árvore"""
        try:
            # Encontrar o arquivo nos dados
            for item in self.files_data:
                if item['id'] == file_data['id']:
                    item['status'] = status
                    break
            
            # Atualizar na árvore se existir
            if file_data['id'] in self.tree_items:
                tree_item = self.tree_items[file_data['id']]['tree_item']
                current_values = list(self.tree.item(tree_item, "values"))
                current_values[3] = status  # Status é a 4ª coluna (índice 3)
                self.tree.item(tree_item, values=current_values)
                
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")
    
    def _download_file(self, file_data):
        try:
            # Pular se for pasta
            if file_data['type'] == 'folder':
                return True
            
            # Obter URL real de download
            download_url = self._get_download_url(file_data['url'])
            if not download_url:
                return False
            
            # Baixar arquivo
            response = self.session.get(download_url, stream=True)
            response.raise_for_status()
            
            # Preparar caminho do arquivo mantendo estrutura de pastas
            file_path = file_data['path']
            # Remover emoji do nome
            clean_path = file_path.replace('📄 ', '').replace('📁 ', '')
            
            # Sanitizar nome do arquivo
            clean_path = re.sub(r'[<>:"/\\|?*]', '_', clean_path)
            
            # Criar caminho completo
            full_path = os.path.join(self.download_folder, clean_path)
            
            # Criar diretórios se necessário
            dir_path = os.path.dirname(full_path)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
            
            # Evitar sobrescrever arquivos
            counter = 1
            original_full_path = full_path
            while os.path.exists(full_path):
                name, ext = os.path.splitext(original_full_path)
                full_path = f"{name}_{counter}{ext}"
                counter += 1
            
            # Salvar arquivo
            with open(full_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            return True
            
        except Exception as e:
            print(f"Erro ao baixar {file_data['name']}: {e}")
            return False
    
    def _get_download_url(self, file_url):
        try:
            response = self.session.get(file_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            scripts = soup.find_all('script')
            
            for script in scripts:
                if script.string:
                    script_content = script.string
                    
                    # Procurar pela URL do S3/Mega
                    s3_pattern = r'downloadUrl\s*=\s*`([^`]+)`'
                    s3_match = re.search(s3_pattern, script_content)
                    
                    if s3_match:
                        return s3_match.group(1)
            
            return None
            
        except Exception as e:
            print(f"Erro ao obter URL de download: {e}")
            return None

def main():
    root = tk.Tk()
    app = DriveDePobreGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
