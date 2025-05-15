from tkinter import Tk, Label, Entry, Button, messagebox
import os
from utils.file_operations import check_file_exists
from utils.tree_generator import generate_tree_diagram
from utils.excel_generator import generate_report_mapeado, generate_report_compilado

class PBIPAnalyzerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Analisador de PBIP")

        self.label = Label(master, text="Caminho do arquivo JSON:")
        self.label.pack()

        self.json_path_entry = Entry(master, width=50)
        self.json_path_entry.pack()

        self.generate_button = Button(master, text="Gerar Documentos", command=self.generate_documents)
        self.generate_button.pack()

        self.json_path_entry.bind("<KeyRelease>", self.check_json_file)

    def check_json_file(self, event):
        json_path = self.json_path_entry.get()
        if os.path.isfile(json_path):
            self.generate_button.config(state="normal")
        else:
            self.generate_button.config(state="disabled")

    def generate_documents(self):
        json_path = self.json_path_entry.get()
        if not os.path.isfile(json_path):
            messagebox.showerror("Erro", "O arquivo JSON especificado não existe.")
            return

        try:
            generate_tree_diagram(json_path)
            generate_report_mapeado(json_path)
            generate_report_compilado(json_path)
            messagebox.showinfo("Sucesso", "Documentos gerados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

if __name__ == "__main__":
    root = Tk()
    gui = PBIPAnalyzerGUI(root)
    root.mainloop()