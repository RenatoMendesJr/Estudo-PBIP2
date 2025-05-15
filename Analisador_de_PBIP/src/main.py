import tkinter as tk
from tkinter import filedialog, messagebox
from utils.file_operations import check_file_exists, create_directory
from utils.json_processing import load_json
from utils.tree_generator import generate_tree_diagram
from utils.excel_generator import generate_report_mapeado, generate_report_compilado
from utils.dataframes_generator import generate_vc_complemento, process_sections
import os
import json
import pandas as pd

class PBIPAnalyzerApp:
    def __init__(self, master):
        self.master = master
        master.title("Analisador de PBIP")

        self.json_file_path = tk.StringVar()

        self.label = tk.Label(master, text="Caminho do arquivo JSON:")
        self.label.pack()

        self.entry = tk.Entry(master, textvariable=self.json_file_path, width=50)
        self.entry.pack()

        self.browse_button = tk.Button(master, text="Procurar", command=self.browse_file)
        self.browse_button.pack()

        self.generate_button = tk.Button(master, text="Gerar Documentos", command=self.generate_documents, state=tk.DISABLED)
        self.generate_button.pack()

        self.json_file_path.trace("w", self.check_file)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.json_file_path.set(file_path)

    def check_file(self, *args):
        if check_file_exists(self.json_file_path.get()):
            self.generate_button.config(state=tk.NORMAL)
        else:
            self.generate_button.config(state=tk.DISABLED)

    def generate_documents(self):
        json_file = self.json_file_path.get()
        if not json_file:
            messagebox.showerror("Erro", "Por favor, selecione um arquivo JSON válido.")
            return

        try:
            data = load_json(json_file)

            # Cria a pasta "Documentos Gerados" dentro do diretório "Analisador_de_PBIP"
            base_dir = os.path.dirname(os.path.dirname(__file__))  # Diretório base do projeto
            output_dir = os.path.join(base_dir, "Documentos Gerados")
            create_directory(output_dir)

            # Define os caminhos de saída para os arquivos gerados
            output_dot_file = os.path.join(output_dir, "tree_diagram.dot")
            output_excel_mapeado = os.path.join(output_dir, "report_mapeado.xlsx")
            output_excel_compilado = os.path.join(output_dir, "report_compilado.xlsx")

            # Gera os documentos
            generate_tree_diagram(data, output_dot_file)
            generate_report_mapeado(data, output_excel_mapeado)

            # Gere os DataFrames necessários
            df_sections, df_visual_containers, df_vc_complemento = process_sections(data)

            # Passe os DataFrames e o caminho de saída para a função
            generate_report_compilado(df_sections, df_visual_containers, df_vc_complemento, output_excel_compilado)

            messagebox.showinfo("Sucesso", f"Documentos gerados com sucesso na pasta:\n{output_dir}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PBIPAnalyzerApp(root)
    root.mainloop()