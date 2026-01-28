#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Controle Financeiro Profissional
Aplicativo Desktop para gerenciamento de finanças pessoais
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime
from typing import List, Dict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Configurações do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ControleFinanceiro:
    def __init__(self):
        self.lancamentos = []
        self.arquivo_dados = "dados_financeiros.json"
        self.carregar_dados()
        
        self.categorias = [
            {"icon": "🍔", "nome": "Alimentação"},
            {"icon": "🏠", "nome": "Moradia"},
            {"icon": "🚗", "nome": "Transporte"},
            {"icon": "🎮", "nome": "Lazer"},
            {"icon": "💊", "nome": "Saúde"},
            {"icon": "📄", "nome": "Contas Fixas"},
            {"icon": "📈", "nome": "Investimentos"},
            {"icon": "💼", "nome": "Renda"},
            {"icon": "🛍️", "nome": "Outros"}
        ]
    
    def carregar_dados(self):
        """Carrega dados salvos do arquivo JSON"""
        if os.path.exists(self.arquivo_dados):
            try:
                with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                    self.lancamentos = json.load(f)
            except:
                self.lancamentos = []
    
    def salvar_dados(self):
        """Salva dados no arquivo JSON"""
        with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
            json.dump(self.lancamentos, f, ensure_ascii=False, indent=2)
    
    def adicionar_lancamento(self, data: str, descricao: str, categoria: str, 
                            entrada: float, saida: float, investimento: float, 
                            desnecessario: bool):
        """Adiciona um novo lançamento"""
        lancamento = {
            "id": len(self.lancamentos) + 1,
            "data": data,
            "descricao": descricao,
            "categoria": categoria,
            "entrada": entrada,
            "saida": saida,
            "investimento": investimento,
            "desnecessario": desnecessario
        }
        self.lancamentos.append(lancamento)
        self.salvar_dados()
    
    def excluir_lancamento(self, lancamento_id: int):
        """Exclui um lançamento pelo ID"""
        self.lancamentos = [l for l in self.lancamentos if l['id'] != lancamento_id]
        self.salvar_dados()
    
    def calcular_resumo(self) -> Dict:
        """Calcula o resumo financeiro"""
        total_entradas = sum(l['entrada'] for l in self.lancamentos)
        total_saidas = sum(l['saida'] for l in self.lancamentos)
        total_investimentos = sum(l['investimento'] for l in self.lancamentos)
        total_desnecessarios = sum(l['saida'] for l in self.lancamentos if l['desnecessario'])
        
        saldo_disponivel = total_entradas - total_saidas - total_investimentos
        patrimonio_total = total_entradas - total_saidas
        percentual_economizado = (patrimonio_total / total_entradas * 100) if total_entradas > 0 else 0
        maior_gasto = max([l['saida'] for l in self.lancamentos], default=0)
        
        return {
            "total_entradas": total_entradas,
            "total_saidas": total_saidas,
            "total_investimentos": total_investimentos,
            "total_desnecessarios": total_desnecessarios,
            "saldo_disponivel": saldo_disponivel,
            "patrimonio_total": patrimonio_total,
            "percentual_economizado": percentual_economizado,
            "maior_gasto": maior_gasto,
            "total_lancamentos": len(self.lancamentos)
        }
    
    def calcular_por_categoria(self) -> Dict:
        """Calcula totais por categoria"""
        categorias = {}
        total_saidas = sum(l['saida'] for l in self.lancamentos)
        
        for cat in self.categorias:
            nome = cat['nome']
            total = sum(l['saida'] for l in self.lancamentos if l['categoria'] == nome)
            count = len([l for l in self.lancamentos if l['categoria'] == nome])
            percent = (total / total_saidas * 100) if total_saidas > 0 else 0
            
            categorias[nome] = {
                "icon": cat['icon'],
                "total": total,
                "percent": percent,
                "count": count
            }
        
        return categorias


class ControleFinanceiroApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.controle = ControleFinanceiro()
        
        # Configurações da janela
        self.title("💰 Controle Financeiro Profissional")
        self.geometry("1400x900")
        
        # Criar interface
        self.criar_interface()
        self.atualizar_dashboard()
    
    def criar_interface(self):
        """Cria a interface do aplicativo"""
        
        # Grid principal
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        # CABEÇALHO
        header_frame = ctk.CTkFrame(self, corner_radius=10, fg_color=("#2C5F8D", "#1a3a52"))
        header_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="💰 CONTROLE FINANCEIRO PROFISSIONAL",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=15)
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Gerencie suas finanças de forma inteligente e profissional",
            font=ctk.CTkFont(size=14),
            text_color="#B0C4DE"
        )
        subtitle_label.pack(pady=(0, 15))
        
        # PAINEL ESQUERDO - Formulário e Tabela
        left_panel = ctk.CTkFrame(self, corner_radius=10)
        left_panel.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="nsew")
        left_panel.grid_rowconfigure(1, weight=1)
        
        # Frame do Formulário
        form_frame = ctk.CTkFrame(left_panel, corner_radius=10)
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        form_title = ctk.CTkLabel(
            form_frame,
            text="📝 Novo Lançamento",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        form_title.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")
        
        # Linha 1: Data, Descrição, Categoria
        ctk.CTkLabel(form_frame, text="Data:", font=ctk.CTkFont(size=12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.data_entry = ctk.CTkEntry(form_frame, width=120)
        self.data_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.data_entry.grid(row=2, column=0, padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="Descrição:", font=ctk.CTkFont(size=12)).grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.descricao_entry = ctk.CTkEntry(form_frame, width=200)
        self.descricao_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="Categoria:", font=ctk.CTkFont(size=12)).grid(row=1, column=2, padx=10, pady=5, sticky="w")
        categorias_nomes = [f"{c['icon']} {c['nome']}" for c in self.controle.categorias]
        self.categoria_combo = ctk.CTkComboBox(form_frame, values=categorias_nomes, width=180)
        self.categoria_combo.grid(row=2, column=2, padx=10, pady=5)
        
        # Linha 2: Valores
        ctk.CTkLabel(form_frame, text="💵 Entrada (R$):", font=ctk.CTkFont(size=12)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entrada_entry = ctk.CTkEntry(form_frame, width=120, placeholder_text="0.00")
        self.entrada_entry.grid(row=4, column=0, padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="💸 Saída (R$):", font=ctk.CTkFont(size=12)).grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.saida_entry = ctk.CTkEntry(form_frame, width=120, placeholder_text="0.00")
        self.saida_entry.grid(row=4, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="📈 Investimento (R$):", font=ctk.CTkFont(size=12)).grid(row=3, column=2, padx=10, pady=5, sticky="w")
        self.investimento_entry = ctk.CTkEntry(form_frame, width=120, placeholder_text="0.00")
        self.investimento_entry.grid(row=4, column=2, padx=10, pady=5)
        
        # Checkbox e botão
        self.desnecessario_var = ctk.BooleanVar()
        desnecessario_check = ctk.CTkCheckBox(
            form_frame,
            text="⚠️ Gasto Desnecessário",
            variable=self.desnecessario_var,
            font=ctk.CTkFont(size=12)
        )
        desnecessario_check.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        
        add_button = ctk.CTkButton(
            form_frame,
            text="➕ Adicionar Lançamento",
            command=self.adicionar_lancamento,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color=("#2C5F8D", "#1a3a52")
        )
        add_button.grid(row=5, column=2, columnspan=2, padx=10, pady=10, sticky="ew")
        
        # Frame da Tabela
        table_frame = ctk.CTkFrame(left_panel, corner_radius=10)
        table_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        table_title = ctk.CTkLabel(
            table_frame,
            text="📊 Histórico de Lançamentos",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        table_title.pack(padx=10, pady=10, anchor="w")
        
        # Treeview para a tabela
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white", 
                       fieldbackground="#2b2b2b", borderwidth=0)
        style.configure("Treeview.Heading", background="#2C5F8D", foreground="white", 
                       font=("Segoe UI", 10, "bold"))
        
        tree_scroll = ctk.CTkScrollableFrame(table_frame, width=850, height=400)
        tree_scroll.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.tree = ttk.Treeview(
            tree_scroll,
            columns=("ID", "Data", "Descrição", "Categoria", "Entrada", "Saída", "Investimento", "Status"),
            show="headings",
            height=15
        )
        
        # Configurar colunas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.heading("Entrada", text="Entrada")
        self.tree.heading("Saída", text="Saída")
        self.tree.heading("Investimento", text="Investimento")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Data", width=100, anchor="center")
        self.tree.column("Descrição", width=200)
        self.tree.column("Categoria", width=120)
        self.tree.column("Entrada", width=100, anchor="e")
        self.tree.column("Saída", width=100, anchor="e")
        self.tree.column("Investimento", width=100, anchor="e")
        self.tree.column("Status", width=80, anchor="center")
        
        self.tree.pack(fill="both", expand=True)
        
        # Botão de excluir
        delete_button = ctk.CTkButton(
            table_frame,
            text="🗑️ Excluir Selecionado",
            command=self.excluir_lancamento,
            font=ctk.CTkFont(size=12),
            fg_color=("#DC143C", "#8B0000"),
            hover_color=("#FF0000", "#A00000")
        )
        delete_button.pack(padx=10, pady=10)
        
        # PAINEL DIREITO - Dashboard
        right_panel = ctk.CTkScrollableFrame(self, corner_radius=10)
        right_panel.grid(row=1, column=1, padx=(5, 10), pady=10, sticky="nsew")
        
        # Resumo Financeiro
        resumo_frame = ctk.CTkFrame(right_panel, corner_radius=10)
        resumo_frame.pack(padx=10, pady=10, fill="x")
        
        resumo_title = ctk.CTkLabel(
            resumo_frame,
            text="💼 Resumo Financeiro",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        resumo_title.pack(padx=10, pady=10)
        
        # Cards de resumo
        self.resumo_cards = {}
        cards_info = [
            ("entradas", "💵 Total Entradas", "#28a745"),
            ("saidas", "💸 Total Saídas", "#dc3545"),
            ("investimentos", "📈 Total Investido", "#007bff"),
            ("desnecessarios", "⚠️ Gastos Desnecessários", "#fd7e14"),
            ("saldo", "💰 Saldo Disponível", "#ffc107"),
            ("patrimonio", "🏦 Patrimônio Total", "#6f42c1")
        ]
        
        for key, label, color in cards_info:
            card = ctk.CTkFrame(resumo_frame, corner_radius=8, fg_color=color)
            card.pack(padx=10, pady=5, fill="x")
            
            ctk.CTkLabel(
                card,
                text=label,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white"
            ).pack(padx=10, pady=(8, 2))
            
            value_label = ctk.CTkLabel(
                card,
                text="R$ 0,00",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="white"
            )
            value_label.pack(padx=10, pady=(2, 8))
            
            self.resumo_cards[key] = value_label
        
        # Status
        self.status_label = ctk.CTkLabel(
            resumo_frame,
            text="✅ POSITIVO",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#28a745"
        )
        self.status_label.pack(pady=10)
        
        # Estatísticas
        stats_frame = ctk.CTkFrame(resumo_frame, corner_radius=8)
        stats_frame.pack(padx=10, pady=10, fill="x")
        
        self.stats_labels = {}
        stats_info = [
            ("economizado", "💡 Economizado"),
            ("maior_gasto", "📉 Maior Gasto"),
            ("lancamentos", "📝 Lançamentos")
        ]
        
        for key, label in stats_info:
            frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
            frame.pack(padx=10, pady=5, fill="x")
            
            ctk.CTkLabel(
                frame,
                text=label,
                font=ctk.CTkFont(size=11)
            ).pack(side="left")
            
            value = ctk.CTkLabel(
                frame,
                text="-",
                font=ctk.CTkFont(size=11, weight="bold")
            )
            value.pack(side="right")
            
            self.stats_labels[key] = value
        
        # Gráficos
        graficos_frame = ctk.CTkFrame(right_panel, corner_radius=10)
        graficos_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        graficos_title = ctk.CTkLabel(
            graficos_frame,
            text="📊 Análise Gráfica",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        graficos_title.pack(padx=10, pady=10)
        
        self.graficos_container = graficos_frame
        
        # Categorias
        categorias_frame = ctk.CTkFrame(right_panel, corner_radius=10)
        categorias_frame.pack(padx=10, pady=10, fill="x")
        
        cat_title = ctk.CTkLabel(
            categorias_frame,
            text="📂 Análise por Categoria",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        cat_title.pack(padx=10, pady=10)
        
        self.categorias_container = ctk.CTkScrollableFrame(categorias_frame, height=300)
        self.categorias_container.pack(padx=10, pady=10, fill="both", expand=True)
    
    def adicionar_lancamento(self):
        """Adiciona um novo lançamento"""
        try:
            data = self.data_entry.get()
            descricao = self.descricao_entry.get()
            categoria_selecionada = self.categoria_combo.get().split(' ', 1)[1]  # Remove emoji
            
            entrada = float(self.entrada_entry.get() or 0)
            saida = float(self.saida_entry.get() or 0)
            investimento = float(self.investimento_entry.get() or 0)
            desnecessario = self.desnecessario_var.get()
            
            if not descricao:
                messagebox.showwarning("Atenção", "Por favor, preencha a descrição!")
                return
            
            self.controle.adicionar_lancamento(
                data, descricao, categoria_selecionada,
                entrada, saida, investimento, desnecessario
            )
            
            # Limpar campos
            self.descricao_entry.delete(0, 'end')
            self.entrada_entry.delete(0, 'end')
            self.saida_entry.delete(0, 'end')
            self.investimento_entry.delete(0, 'end')
            self.desnecessario_var.set(False)
            self.data_entry.delete(0, 'end')
            self.data_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            
            self.atualizar_dashboard()
            messagebox.showinfo("Sucesso", "Lançamento adicionado com sucesso!")
            
        except ValueError:
            messagebox.showerror("Erro", "Valores numéricos inválidos!")
    
    def excluir_lancamento(self):
        """Exclui o lançamento selecionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione um lançamento para excluir!")
            return
        
        item = self.tree.item(selected[0])
        lancamento_id = int(item['values'][0])
        
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este lançamento?"):
            self.controle.excluir_lancamento(lancamento_id)
            self.atualizar_dashboard()
            messagebox.showinfo("Sucesso", "Lançamento excluído com sucesso!")
    
    def atualizar_dashboard(self):
        """Atualiza todos os dados do dashboard"""
        # Atualizar tabela
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for lancamento in sorted(self.controle.lancamentos, key=lambda x: x['data'], reverse=True):
            entrada = f"R$ {lancamento['entrada']:.2f}" if lancamento['entrada'] > 0 else "-"
            saida = f"R$ {lancamento['saida']:.2f}" if lancamento['saida'] > 0 else "-"
            investimento = f"R$ {lancamento['investimento']:.2f}" if lancamento['investimento'] > 0 else "-"
            status = "⚠️" if lancamento['desnecessario'] else "✓"
            
            # Buscar ícone da categoria
            cat_icon = next((c['icon'] for c in self.controle.categorias if c['nome'] == lancamento['categoria']), '')
            categoria_display = f"{cat_icon} {lancamento['categoria']}"
            
            self.tree.insert("", "end", values=(
                lancamento['id'],
                lancamento['data'],
                lancamento['descricao'],
                categoria_display,
                entrada,
                saida,
                investimento,
                status
            ))
        
        # Atualizar resumo
        resumo = self.controle.calcular_resumo()
        
        self.resumo_cards['entradas'].configure(text=f"R$ {resumo['total_entradas']:,.2f}")
        self.resumo_cards['saidas'].configure(text=f"R$ {resumo['total_saidas']:,.2f}")
        self.resumo_cards['investimentos'].configure(text=f"R$ {resumo['total_investimentos']:,.2f}")
        self.resumo_cards['desnecessarios'].configure(text=f"R$ {resumo['total_desnecessarios']:,.2f}")
        self.resumo_cards['saldo'].configure(text=f"R$ {resumo['saldo_disponivel']:,.2f}")
        self.resumo_cards['patrimonio'].configure(text=f"R$ {resumo['patrimonio_total']:,.2f}")
        
        # Atualizar status
        if resumo['patrimonio_total'] > 0:
            self.status_label.configure(text="✅ POSITIVO", text_color="#28a745")
        else:
            self.status_label.configure(text="❌ ENDIVIDADO", text_color="#dc3545")
        
        # Atualizar estatísticas
        self.stats_labels['economizado'].configure(text=f"{resumo['percentual_economizado']:.1f}%")
        self.stats_labels['maior_gasto'].configure(text=f"R$ {resumo['maior_gasto']:,.2f}")
        self.stats_labels['lancamentos'].configure(text=str(resumo['total_lancamentos']))
        
        # Atualizar gráficos
        self.atualizar_graficos()
        
        # Atualizar categorias
        self.atualizar_categorias()
    
    def atualizar_graficos(self):
        """Atualiza os gráficos"""
        # Limpar gráficos antigos
        for widget in self.graficos_container.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.get_tk_widget().destroy()
        
        categorias = self.controle.calcular_por_categoria()
        
        # Filtrar categorias com valores
        categorias_com_valores = {k: v for k, v in categorias.items() if v['total'] > 0}
        
        if not categorias_com_valores:
            return
        
        # Criar figura
        fig = Figure(figsize=(5, 4), facecolor='#2b2b2b')
        ax = fig.add_subplot(111)
        
        labels = [f"{v['icon']} {k}" for k, v in categorias_com_valores.items()]
        values = [v['total'] for v in categorias_com_valores.values()]
        colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#2193b0', '#C9CBCF']
        
        ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, 
               textprops={'color': 'white', 'fontsize': 9})
        ax.set_title('Distribuição de Gastos', color='white', fontsize=12, pad=20)
        
        # Canvas
        canvas = FigureCanvasTkAgg(fig, master=self.graficos_container)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10)
    
    def atualizar_categorias(self):
        """Atualiza a lista de categorias"""
        # Limpar
        for widget in self.categorias_container.winfo_children():
            widget.destroy()
        
        categorias = self.controle.calcular_por_categoria()
        
        for nome, dados in categorias.items():
            if dados['total'] > 0 or dados['count'] > 0:
                cat_frame = ctk.CTkFrame(self.categorias_container, corner_radius=8)
                cat_frame.pack(padx=5, pady=5, fill="x")
                
                # Lado esquerdo
                left = ctk.CTkFrame(cat_frame, fg_color="transparent")
                left.pack(side="left", padx=10, pady=8)
                
                ctk.CTkLabel(
                    left,
                    text=dados['icon'],
                    font=ctk.CTkFont(size=24)
                ).pack(side="left", padx=5)
                
                info_frame = ctk.CTkFrame(left, fg_color="transparent")
                info_frame.pack(side="left", padx=5)
                
                ctk.CTkLabel(
                    info_frame,
                    text=nome,
                    font=ctk.CTkFont(size=12, weight="bold")
                ).pack(anchor="w")
                
                ctk.CTkLabel(
                    info_frame,
                    text=f"{dados['count']} lançamento{'s' if dados['count'] != 1 else ''}",
                    font=ctk.CTkFont(size=10),
                    text_color="gray"
                ).pack(anchor="w")
                
                # Lado direito
                right = ctk.CTkFrame(cat_frame, fg_color="transparent")
                right.pack(side="right", padx=10, pady=8)
                
                ctk.CTkLabel(
                    right,
                    text=f"R$ {dados['total']:,.2f}",
                    font=ctk.CTkFont(size=14, weight="bold")
                ).pack(anchor="e")
                
                ctk.CTkLabel(
                    right,
                    text=f"{dados['percent']:.1f}% do total",
                    font=ctk.CTkFont(size=10),
                    text_color="gray"
                ).pack(anchor="e")


def main():
    app = ControleFinanceiroApp()
    app.mainloop()


if __name__ == "__main__":
    main()
