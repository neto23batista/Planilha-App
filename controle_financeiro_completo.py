#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Controle Financeiro Profissional - Aplicativo Desktop
Versão Python baseada no sistema HTML completo
"""

import customtkinter as ctk
from tkinter import messagebox
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Configurações do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ControleFinanceiro:
    """Classe para gerenciar dados financeiros"""
    
    def __init__(self):
        self.lancamentos = []
        self.contasFixas = []
        self.arquivo_dados = "dados_financeiros.json"
        self.arquivo_contas_fixas = "contas_fixas.json"
        self.carregar_dados()
        
        self.categorias = {
            'Alimentação': '🍔',
            'Moradia': '🏠',
            'Transporte': '🚗',
            'Lazer': '🎮',
            'Saúde': '💊',
            'Contas Fixas': '📄',
            'Investimentos': '📈',
            'Renda': '💼',
            'Outros': '🛍️'
        }
        
        self.verificar_contas_fixas_do_mes()
    
    def carregar_dados(self):
        """Carrega dados dos arquivos JSON"""
        if os.path.exists(self.arquivo_dados):
            try:
                with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                    self.lancamentos = json.load(f)
            except:
                self.lancamentos = []
        
        if os.path.exists(self.arquivo_contas_fixas):
            try:
                with open(self.arquivo_contas_fixas, 'r', encoding='utf-8') as f:
                    self.contasFixas = json.load(f)
            except:
                self.contasFixas = []
    
    def salvar_dados(self):
        """Salva dados nos arquivos JSON"""
        with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
            json.dump(self.lancamentos, f, ensure_ascii=False, indent=2)
        
        with open(self.arquivo_contas_fixas, 'w', encoding='utf-8') as f:
            json.dump(self.contasFixas, f, ensure_ascii=False, indent=2)
    
    def verificar_contas_fixas_do_mes(self):
        """Gera lançamentos automáticos das contas fixas para o mês atual"""
        mes_atual = datetime.now().strftime("%Y-%m")
        arquivo_controle = "ultimo_mes_contas_fixas.txt"
        
        ultimo_mes = ""
        if os.path.exists(arquivo_controle):
            with open(arquivo_controle, 'r') as f:
                ultimo_mes = f.read().strip()
        
        if ultimo_mes != mes_atual and self.contasFixas:
            dia_atual = datetime.now().day
            
            for conta in self.contasFixas:
                # Verifica se já existe lançamento desta conta fixa no mês
                ja_existe = any(
                    l.get('contaFixaId') == conta['id'] and 
                    l['data'].startswith(mes_atual)
                    for l in self.lancamentos
                )
                
                if not ja_existe:
                    novo_lancamento = {
                        'id': self._gerar_id(),
                        'data': f"{mes_atual}-{dia_atual:02d}",
                        'descricao': conta['descricao'],
                        'categoria': conta['categoria'],
                        'entrada': conta.get('entrada', 0),
                        'saida': conta.get('saida', 0),
                        'investimento': conta.get('investimento', 0),
                        'statusPagamento': 'nao-paga',
                        'desnecessario': False,
                        'recorrente': False,
                        'contaFixaId': conta['id']
                    }
                    self.lancamentos.append(novo_lancamento)
            
            with open(arquivo_controle, 'w') as f:
                f.write(mes_atual)
            
            self.salvar_dados()
    
    def _gerar_id(self):
        """Gera um ID único"""
        import time
        return int(time.time() * 1000)
    
    def adicionar(self, lancamento):
        """Adiciona um novo lançamento"""
        lancamento['id'] = self._gerar_id()
        
        # Se for parcelado, criar as parcelas
        if lancamento.get('parcelas') and lancamento['parcelas'] >= 2:
            self.criar_parcelas(lancamento)
        else:
            # Se for recorrente (conta fixa)
            if lancamento.get('recorrente'):
                conta_fixa = {
                    'id': self._gerar_id(),
                    'descricao': lancamento['descricao'],
                    'categoria': lancamento['categoria'],
                    'entrada': lancamento.get('entrada', 0),
                    'saida': lancamento.get('saida', 0),
                    'investimento': lancamento.get('investimento', 0),
                    'desnecessario': lancamento.get('desnecessario', False)
                }
                self.contasFixas.append(conta_fixa)
                lancamento['contaFixaId'] = conta_fixa['id']
            
            self.lancamentos.append(lancamento)
        
        self.salvar_dados()
    
    def criar_parcelas(self, lancamento_original):
        """Cria lançamentos parcelados"""
        data_inicial = datetime.strptime(lancamento_original['data'], '%Y-%m-%d')
        valor_total = (lancamento_original.get('entrada', 0) or 
                      lancamento_original.get('saida', 0) or 
                      lancamento_original.get('investimento', 0))
        valor_parcela = valor_total / lancamento_original['parcelas']
        grupo_parcela_id = self._gerar_id()
        
        for i in range(lancamento_original['parcelas']):
            data_parcela = data_inicial + timedelta(days=30 * i)
            
            parcela = {
                'id': self._gerar_id() + i,
                'data': data_parcela.strftime('%Y-%m-%d'),
                'descricao': lancamento_original['descricao'],
                'descricaoOriginal': lancamento_original['descricao'],
                'categoria': lancamento_original['categoria'],
                'entrada': valor_parcela if lancamento_original.get('entrada', 0) > 0 else 0,
                'saida': valor_parcela if lancamento_original.get('saida', 0) > 0 else 0,
                'investimento': valor_parcela if lancamento_original.get('investimento', 0) > 0 else 0,
                'statusPagamento': 'paga' if i == 0 and lancamento_original.get('statusPagamento') == 'paga' else 'nao-paga',
                'desnecessario': lancamento_original.get('desnecessario', False),
                'recorrente': False,
                'parcelaAtual': i + 1,
                'totalParcelas': lancamento_original['parcelas'],
                'grupoParcelaId': grupo_parcela_id
            }
            
            self.lancamentos.append(parcela)
    
    def excluir(self, lancamento_id):
        """Exclui um lançamento"""
        self.lancamentos = [l for l in self.lancamentos if l['id'] != lancamento_id]
        self.salvar_dados()
    
    def excluir_grupo_parcelamento(self, grupo_id):
        """Exclui todas as parcelas de um grupo"""
        self.lancamentos = [l for l in self.lancamentos if l.get('grupoParcelaId') != grupo_id]
        self.salvar_dados()
    
    def excluir_conta_fixa(self, conta_id):
        """Exclui uma conta fixa e todos seus lançamentos"""
        self.contasFixas = [c for c in self.contasFixas if c['id'] != conta_id]
        self.lancamentos = [l for l in self.lancamentos if l.get('contaFixaId') != conta_id]
        self.salvar_dados()
    
    def alterar_status_pagamento(self, lancamento_id, novo_status):
        """Altera o status de pagamento de um lançamento"""
        for lancamento in self.lancamentos:
            if lancamento['id'] == lancamento_id:
                lancamento['statusPagamento'] = novo_status
                break
        self.salvar_dados()
    
    def obter_lancamentos_mes_atual(self):
        """Retorna apenas lançamentos do mês atual"""
        mes_atual = datetime.now().strftime("%Y-%m")
        return [l for l in self.lancamentos if l['data'].startswith(mes_atual)]
    
    def obter_parcelamentos(self):
        """Retorna resumo de todos os parcelamentos"""
        grupos = {}
        
        for l in self.lancamentos:
            if l.get('grupoParcelaId'):
                grupo_id = l['grupoParcelaId']
                if grupo_id not in grupos:
                    grupos[grupo_id] = {
                        'id': grupo_id,
                        'descricao': l.get('descricaoOriginal', l['descricao'].split(' (')[0]),
                        'categoria': l['categoria'],
                        'totalParcelas': l['totalParcelas'],
                        'valorParcela': l.get('entrada', 0) or l.get('saida', 0) or l.get('investimento', 0),
                        'tipo': 'entrada' if l.get('entrada', 0) > 0 else 'saida' if l.get('saida', 0) > 0 else 'investimento',
                        'parcelas': []
                    }
                grupos[grupo_id]['parcelas'].append(l)
        
        # Calcular estatísticas
        for grupo in grupos.values():
            grupo['parcelas'].sort(key=lambda x: x['data'])
            grupo['parcelasPagas'] = sum(1 for p in grupo['parcelas'] if p['statusPagamento'] == 'paga')
            grupo['valorTotal'] = grupo['valorParcela'] * grupo['totalParcelas']
            grupo['valorPago'] = grupo['valorParcela'] * grupo['parcelasPagas']
            grupo['valorRestante'] = grupo['valorTotal'] - grupo['valorPago']
        
        return list(grupos.values())
    
    def calcular_resumo(self):
        """Calcula o resumo financeiro"""
        total_entradas = sum(l.get('entrada', 0) for l in self.lancamentos)
        total_saidas = sum(l.get('saida', 0) for l in self.lancamentos)
        total_investimentos = sum(l.get('investimento', 0) for l in self.lancamentos)
        total_desnecessarios = sum(l.get('saida', 0) for l in self.lancamentos if l.get('desnecessario'))
        total_nao_pagas = sum(1 for l in self.lancamentos if l.get('statusPagamento') == 'nao-paga')
        
        return {
            'totalEntradas': total_entradas,
            'totalSaidas': total_saidas,
            'totalInvestimentos': total_investimentos,
            'totalDesnecessarios': total_desnecessarios,
            'saldoDisponivel': total_entradas - total_saidas - total_investimentos,
            'patrimonioTotal': total_entradas - total_saidas,
            'percentualEconomizado': (total_entradas - total_saidas) / total_entradas * 100 if total_entradas > 0 else 0,
            'maiorGasto': max([l.get('saida', 0) for l in self.lancamentos], default=0),
            'totalLancamentos': len(self.lancamentos),
            'totalNaoPagas': total_nao_pagas
        }
    
    def calcular_por_categoria(self):
        """Calcula totais por categoria"""
        resultado = {}
        total_saidas = sum(l.get('saida', 0) for l in self.lancamentos)
        
        for nome_cat, icon in self.categorias.items():
            total = sum(l.get('saida', 0) for l in self.lancamentos if l.get('categoria') == nome_cat)
            count = sum(1 for l in self.lancamentos if l.get('categoria') == nome_cat)
            percent = (total / total_saidas * 100) if total_saidas > 0 else 0
            
            resultado[nome_cat] = {
                'icon': icon,
                'total': total,
                'percent': percent,
                'count': count
            }
        
        return resultado


class ControleFinanceiroApp(ctk.CTk):
    """Interface gráfica do aplicativo"""
    
    def __init__(self):
        super().__init__()
        
        self.controle = ControleFinanceiro()
        
        # Configurações da janela
        self.title("💰 Controle Financeiro Profissional")
        self.geometry("1600x950")
        
        # Criar interface
        self.criar_interface()
        self.atualizar_dashboard()
    
    def criar_interface(self):
        """Cria a interface completa do aplicativo"""
        
        # Grid principal
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        
        # ===== CABEÇALHO =====
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
            text="Gerencie suas finanças de forma inteligente e visual",
            font=ctk.CTkFont(size=14),
            text_color="#B0C4DE"
        )
        subtitle_label.pack(pady=(0, 15))
        
        # ===== PAINEL ESQUERDO =====
        left_panel = ctk.CTkScrollableFrame(self, corner_radius=10)
        left_panel.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="nsew")
        
        self.criar_formulario(left_panel)
        self.criar_abas_tabelas(left_panel)
        
        # ===== PAINEL DIREITO =====
        right_panel = ctk.CTkScrollableFrame(self, corner_radius=10)
        right_panel.grid(row=1, column=1, padx=(5, 10), pady=10, sticky="nsew")
        
        self.criar_resumo(right_panel)
        self.criar_categorias(right_panel)
    
    def criar_formulario(self, parent):
        """Cria o formulário de lançamento"""
        form_frame = ctk.CTkFrame(parent, corner_radius=10)
        form_frame.pack(padx=10, pady=10, fill="x")
        
        form_title = ctk.CTkLabel(
            form_frame,
            text="📝 Novo Lançamento",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        form_title.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")
        
        # Linha 1
        ctk.CTkLabel(form_frame, text="Data:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.data_entry = ctk.CTkEntry(form_frame, width=120)
        self.data_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.data_entry.grid(row=2, column=0, padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="Descrição:").grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.descricao_entry = ctk.CTkEntry(form_frame, width=200)
        self.descricao_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="Categoria:").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        categorias_nomes = [f"{v} {k}" for k, v in self.controle.categorias.items()]
        self.categoria_combo = ctk.CTkComboBox(form_frame, values=categorias_nomes, width=180)
        self.categoria_combo.grid(row=2, column=2, padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="Status Pagamento:").grid(row=1, column=3, padx=10, pady=5, sticky="w")
        self.status_combo = ctk.CTkComboBox(
            form_frame,
            values=["✅ Paga", "❌ Não Paga", "💳 Parcelada"],
            width=150
        )
        self.status_combo.grid(row=2, column=3, padx=10, pady=5)
        
        # Linha 2
        ctk.CTkLabel(form_frame, text="💵 Entrada (R$):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entrada_entry = ctk.CTkEntry(form_frame, width=120, placeholder_text="0.00")
        self.entrada_entry.grid(row=4, column=0, padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="💸 Saída (R$):").grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.saida_entry = ctk.CTkEntry(form_frame, width=120, placeholder_text="0.00")
        self.saida_entry.grid(row=4, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="📈 Investimento (R$):").grid(row=3, column=2, padx=10, pady=5, sticky="w")
        self.investimento_entry = ctk.CTkEntry(form_frame, width=120, placeholder_text="0.00")
        self.investimento_entry.grid(row=4, column=2, padx=10, pady=5)
        
        ctk.CTkLabel(form_frame, text="📦 Parcelas:").grid(row=3, column=3, padx=10, pady=5, sticky="w")
        self.parcelas_entry = ctk.CTkEntry(form_frame, width=120, placeholder_text="Ex: 12")
        self.parcelas_entry.grid(row=4, column=3, padx=10, pady=5)
        
        # Checkboxes
        self.desnecessario_var = ctk.BooleanVar()
        desnecessario_check = ctk.CTkCheckBox(
            form_frame,
            text="⚠️ Gasto Desnecessário",
            variable=self.desnecessario_var
        )
        desnecessario_check.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="w")
        
        self.recorrente_var = ctk.BooleanVar()
        recorrente_check = ctk.CTkCheckBox(
            form_frame,
            text="🔄 Conta Fixa Recorrente",
            variable=self.recorrente_var
        )
        recorrente_check.grid(row=5, column=2, columnspan=2, padx=10, pady=10, sticky="w")
        
        # Botão adicionar
        add_button = ctk.CTkButton(
            form_frame,
            text="➕ Adicionar Lançamento",
            command=self.adicionar_lancamento,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            fg_color=("#2C5F8D", "#1a3a52")
        )
        add_button.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
    
    def criar_abas_tabelas(self, parent):
        """Cria as abas com tabelas"""
        tabs_frame = ctk.CTkFrame(parent, corner_radius=10)
        tabs_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Criar notebook de abas
        self.tabview = ctk.CTkTabview(tabs_frame)
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Adicionar abas
        self.tabview.add("📊 Lançamentos do Mês")
        self.tabview.add("💳 Parcelamentos")
        self.tabview.add("🔄 Contas Fixas")
        
        # Conteúdo das abas será criado dinamicamente
        self.criar_tab_lancamentos()
        self.criar_tab_parcelamentos()
        self.criar_tab_contas_fixas()
    
    def criar_tab_lancamentos(self):
        """Cria conteúdo da aba de lançamentos"""
        tab = self.tabview.tab("📊 Lançamentos do Mês")
        
        # Frame para a lista
        self.lancamentos_frame = ctk.CTkScrollableFrame(tab, height=400)
        self.lancamentos_frame.pack(padx=10, pady=10, fill="both", expand=True)
    
    def criar_tab_parcelamentos(self):
        """Cria conteúdo da aba de parcelamentos"""
        tab = self.tabview.tab("💳 Parcelamentos")
        
        self.parcelamentos_frame = ctk.CTkScrollableFrame(tab, height=400)
        self.parcelamentos_frame.pack(padx=10, pady=10, fill="both", expand=True)
    
    def criar_tab_contas_fixas(self):
        """Cria conteúdo da aba de contas fixas"""
        tab = self.tabview.tab("🔄 Contas Fixas")
        
        self.contas_fixas_frame = ctk.CTkScrollableFrame(tab, height=400)
        self.contas_fixas_frame.pack(padx=10, pady=10, fill="both", expand=True)
    
    def criar_resumo(self, parent):
        """Cria o resumo financeiro"""
        resumo_frame = ctk.CTkFrame(parent, corner_radius=10)
        resumo_frame.pack(padx=10, pady=10, fill="x")
        
        resumo_title = ctk.CTkLabel(
            resumo_frame,
            text="💼 Resumo Financeiro",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        resumo_title.pack(padx=10, pady=10)
        
        # Cards de resumo
        self.resumo_labels = {}
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
            
            self.resumo_labels[key] = value_label
        
        # Status
        self.status_label = ctk.CTkLabel(
            resumo_frame,
            text="✅ POSITIVO",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#28a745"
        )
        self.status_label.pack(pady=10)
        
        # Estatísticas
        stats_frame = ctk.CTkFrame(resumo_frame)
        stats_frame.pack(padx=10, pady=10, fill="x")
        
        self.stats_labels = {}
        stats_info = [
            ("economizado", "💡 Economizado"),
            ("maior_gasto", "📉 Maior Gasto"),
            ("lancamentos", "📝 Lançamentos"),
            ("nao_pagas", "❌ Não Pagas")
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
    
    def criar_categorias(self, parent):
        """Cria a seção de categorias"""
        categorias_frame = ctk.CTkFrame(parent, corner_radius=10)
        categorias_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        cat_title = ctk.CTkLabel(
            categorias_frame,
            text="📂 Análise por Categoria",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        cat_title.pack(padx=10, pady=10)
        
        self.categorias_container = ctk.CTkScrollableFrame(categorias_frame, height=400)
        self.categorias_container.pack(padx=10, pady=10, fill="both", expand=True)
    
    def adicionar_lancamento(self):
        """Adiciona um novo lançamento"""
        try:
            data = self.data_entry.get()
            descricao = self.descricao_entry.get()
            categoria_selecionada = self.categoria_combo.get().split(' ', 1)[1]
            
            entrada = float(self.entrada_entry.get() or 0)
            saida = float(self.saida_entry.get() or 0)
            investimento = float(self.investimento_entry.get() or 0)
            parcelas = int(self.parcelas_entry.get() or 0)
            
            status_map = {"✅ Paga": "paga", "❌ Não Paga": "nao-paga", "💳 Parcelada": "parcelada"}
            status = status_map.get(self.status_combo.get(), "nao-paga")
            
            if not descricao:
                messagebox.showwarning("Atenção", "Por favor, preencha a descrição!")
                return
            
            lancamento = {
                'data': data,
                'descricao': descricao,
                'categoria': categoria_selecionada,
                'entrada': entrada,
                'saida': saida,
                'investimento': investimento,
                'statusPagamento': status,
                'parcelas': parcelas if parcelas >= 2 else None,
                'desnecessario': self.desnecessario_var.get(),
                'recorrente': self.recorrente_var.get() and parcelas < 2
            }
            
            self.controle.adicionar(lancamento)
            
            # Limpar campos
            self.descricao_entry.delete(0, 'end')
            self.entrada_entry.delete(0, 'end')
            self.saida_entry.delete(0, 'end')
            self.investimento_entry.delete(0, 'end')
            self.parcelas_entry.delete(0, 'end')
            self.desnecessario_var.set(False)
            self.recorrente_var.set(False)
            self.data_entry.delete(0, 'end')
            self.data_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
            
            self.atualizar_dashboard()
            
            mensagem = "✅ Lançamento adicionado com sucesso!"
            if parcelas >= 2:
                mensagem += f"\n💳 {parcelas} parcelas criadas automaticamente!"
            elif lancamento['recorrente']:
                mensagem += "\n🔄 Conta fixa cadastrada!"
            
            messagebox.showinfo("Sucesso", mensagem)
            
        except ValueError:
            messagebox.showerror("Erro", "Valores numéricos inválidos!")
    
    def atualizar_dashboard(self):
        """Atualiza todos os dados do dashboard"""
        resumo = self.controle.calcular_resumo()
        
        # Atualizar resumo
        self.resumo_labels['entradas'].configure(text=f"R$ {resumo['totalEntradas']:,.2f}")
        self.resumo_labels['saidas'].configure(text=f"R$ {resumo['totalSaidas']:,.2f}")
        self.resumo_labels['investimentos'].configure(text=f"R$ {resumo['totalInvestimentos']:,.2f}")
        self.resumo_labels['desnecessarios'].configure(text=f"R$ {resumo['totalDesnecessarios']:,.2f}")
        self.resumo_labels['saldo'].configure(text=f"R$ {resumo['saldoDisponivel']:,.2f}")
        self.resumo_labels['patrimonio'].configure(text=f"R$ {resumo['patrimonioTotal']:,.2f}")
        
        # Status
        if resumo['patrimonioTotal'] > 0:
            self.status_label.configure(text="✅ POSITIVO", text_color="#28a745")
        else:
            self.status_label.configure(text="❌ ENDIVIDADO", text_color="#dc3545")
        
        # Estatísticas
        self.stats_labels['economizado'].configure(text=f"{resumo['percentualEconomizado']:.1f}%")
        self.stats_labels['maior_gasto'].configure(text=f"R$ {resumo['maiorGasto']:,.2f}")
        self.stats_labels['lancamentos'].configure(text=str(resumo['totalLancamentos']))
        self.stats_labels['nao_pagas'].configure(text=str(resumo['totalNaoPagas']))
        
        # Atualizar tabelas
        self.atualizar_lancamentos()
        self.atualizar_parcelamentos()
        self.atualizar_contas_fixas()
        self.atualizar_categorias()
    
    def atualizar_lancamentos(self):
        """Atualiza a lista de lançamentos do mês"""
        # Limpar frame
        for widget in self.lancamentos_frame.winfo_children():
            widget.destroy()
        
        lancamentos_mes = self.controle.obter_lancamentos_mes_atual()
        
        if not lancamentos_mes:
            ctk.CTkLabel(
                self.lancamentos_frame,
                text="📭 Nenhum lançamento neste mês",
                font=ctk.CTkFont(size=14)
            ).pack(pady=50)
            return
        
        # Ordenar por data (mais recente primeiro)
        lancamentos_mes.sort(key=lambda x: x['data'], reverse=True)
        
        for lanc in lancamentos_mes:
            self.criar_card_lancamento(lanc)
    
    def criar_card_lancamento(self, lancamento):
        """Cria um card para um lançamento"""
        card = ctk.CTkFrame(self.lancamentos_frame, corner_radius=10)
        card.pack(padx=5, pady=5, fill="x")
        
        # Linha principal
        main_frame = ctk.CTkFrame(card, fg_color="transparent")
        main_frame.pack(fill="x", padx=10, pady=5)
        
        # Data e descrição
        data_formatada = datetime.strptime(lancamento['data'], '%Y-%m-%d').strftime('%d/%m/%Y')
        icon = self.controle.categorias.get(lancamento['categoria'], '')
        
        info_text = f"{data_formatada} | {icon} {lancamento['descricao']}"
        if lancamento.get('parcelaAtual'):
            info_text += f" ({lancamento['parcelaAtual']}/{lancamento['totalParcelas']})"
        
        ctk.CTkLabel(
            main_frame,
            text=info_text,
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=5)
        
        # Valor
        valor = lancamento.get('entrada', 0) or lancamento.get('saida', 0) or lancamento.get('investimento', 0)
        cor = "#28a745" if lancamento.get('entrada', 0) > 0 else "#dc3545" if lancamento.get('saida', 0) > 0 else "#007bff"
        
        ctk.CTkLabel(
            main_frame,
            text=f"R$ {valor:,.2f}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=cor
        ).pack(side="right", padx=5)
        
        # Botões de ação
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        if lancamento['statusPagamento'] != 'paga':
            ctk.CTkButton(
                btn_frame,
                text="✅ Pagar",
                command=lambda l=lancamento: self.marcar_como_paga(l['id']),
                width=80,
                height=30,
                fg_color="#28a745"
            ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Excluir",
            command=lambda l=lancamento: self.excluir_lancamento(l['id']),
            width=80,
            height=30,
            fg_color="#dc3545"
        ).pack(side="left", padx=2)
        
        # Status
        status_colors = {'paga': '#28a745', 'nao-paga': '#dc3545', 'parcelada': '#ffc107'}
        status_text = {'paga': '✅ Paga', 'nao-paga': '❌ Não Paga', 'parcelada': '💳 Parcelada'}
        
        ctk.CTkLabel(
            btn_frame,
            text=status_text.get(lancamento['statusPagamento'], ''),
            text_color=status_colors.get(lancamento['statusPagamento'], 'white'),
            font=ctk.CTkFont(size=10, weight="bold")
        ).pack(side="right", padx=5)
    
    def atualizar_parcelamentos(self):
        """Atualiza a lista de parcelamentos"""
        for widget in self.parcelamentos_frame.winfo_children():
            widget.destroy()
        
        parcelamentos = self.controle.obter_parcelamentos()
        
        if not parcelamentos:
            ctk.CTkLabel(
                self.parcelamentos_frame,
                text="💳 Nenhum parcelamento ativo",
                font=ctk.CTkFont(size=14)
            ).pack(pady=50)
            return
        
        for parc in parcelamentos:
            self.criar_card_parcelamento(parc)
    
    def criar_card_parcelamento(self, parcelamento):
        """Cria um card para um parcelamento"""
        card = ctk.CTkFrame(self.parcelamentos_frame, corner_radius=10, border_width=2, border_color="#17a2b8")
        card.pack(padx=5, pady=10, fill="x")
        
        # Cabeçalho
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=10)
        
        icon = self.controle.categorias.get(parcelamento['categoria'], '')
        ctk.CTkLabel(
            header,
            text=f"{icon} {parcelamento['descricao']}",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")
        
        ctk.CTkButton(
            header,
            text="🗑️ Excluir Tudo",
            command=lambda p=parcelamento: self.excluir_parcelamento(p['id']),
            width=100,
            height=30,
            fg_color="#dc3545"
        ).pack(side="right")
        
        # Informações
        info_frame = ctk.CTkFrame(card)
        info_frame.pack(fill="x", padx=10, pady=5)
        
        infos = [
            ("Valor Total", f"R$ {parcelamento['valorTotal']:,.2f}"),
            ("Parcela", f"R$ {parcelamento['valorParcela']:,.2f}"),
            ("Parcelas Pagas", f"{parcelamento['parcelasPagas']}/{parcelamento['totalParcelas']}"),
            ("Valor Pago", f"R$ {parcelamento['valorPago']:,.2f}"),
            ("Restante", f"R$ {parcelamento['valorRestante']:,.2f}")
        ]
        
        for i, (label, value) in enumerate(infos):
            frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            frame.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="ew")
            
            ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=10)).pack()
            ctk.CTkLabel(frame, text=value, font=ctk.CTkFont(size=11, weight="bold")).pack()
        
        # Progresso
        percentual = (parcelamento['parcelasPagas'] / parcelamento['totalParcelas']) * 100
        ctk.CTkProgressBar(card, progress_color="#28a745").pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(
            card,
            text=f"{percentual:.1f}% pago",
            font=ctk.CTkFont(size=10)
        ).pack(pady=(0, 10))
    
    def atualizar_contas_fixas(self):
        """Atualiza a lista de contas fixas"""
        for widget in self.contas_fixas_frame.winfo_children():
            widget.destroy()
        
        if not self.controle.contasFixas:
            ctk.CTkLabel(
                self.contas_fixas_frame,
                text="🔄 Nenhuma conta fixa cadastrada",
                font=ctk.CTkFont(size=14)
            ).pack(pady=50)
            return
        
        for conta in self.controle.contasFixas:
            self.criar_card_conta_fixa(conta)
    
    def criar_card_conta_fixa(self, conta):
        """Cria um card para uma conta fixa"""
        card = ctk.CTkFrame(self.contas_fixas_frame, corner_radius=10, border_width=2, border_color="#6f42c1")
        card.pack(padx=5, pady=5, fill="x")
        
        main_frame = ctk.CTkFrame(card, fg_color="transparent")
        main_frame.pack(fill="x", padx=10, pady=10)
        
        icon = self.controle.categorias.get(conta['categoria'], '')
        ctk.CTkLabel(
            main_frame,
            text=f"{icon} {conta['descricao']} 🔄",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")
        
        valor = conta.get('entrada', 0) or conta.get('saida', 0) or conta.get('investimento', 0)
        cor = "#28a745" if conta.get('entrada', 0) > 0 else "#dc3545"
        
        ctk.CTkLabel(
            main_frame,
            text=f"R$ {valor:,.2f}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=cor
        ).pack(side="right", padx=10)
        
        ctk.CTkButton(
            main_frame,
            text="🗑️ Excluir",
            command=lambda c=conta: self.excluir_conta_fixa(c['id']),
            width=80,
            height=30,
            fg_color="#dc3545"
        ).pack(side="right")
    
    def atualizar_categorias(self):
        """Atualiza a lista de categorias"""
        for widget in self.categorias_container.winfo_children():
            widget.destroy()
        
        categorias = self.controle.calcular_por_categoria()
        
        for nome, dados in categorias.items():
            if dados['total'] > 0:
                card = ctk.CTkFrame(self.categorias_container, corner_radius=8)
                card.pack(padx=5, pady=5, fill="x")
                
                frame = ctk.CTkFrame(card, fg_color="transparent")
                frame.pack(fill="x", padx=10, pady=10)
                
                ctk.CTkLabel(
                    frame,
                    text=f"{dados['icon']} {nome}",
                    font=ctk.CTkFont(size=12, weight="bold")
                ).pack(side="left")
                
                ctk.CTkLabel(
                    frame,
                    text=f"R$ {dados['total']:,.2f}",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color="#4a9eff"
                ).pack(side="right")
    
    def marcar_como_paga(self, lancamento_id):
        """Marca um lançamento como pago"""
        self.controle.alterar_status_pagamento(lancamento_id, 'paga')
        self.atualizar_dashboard()
    
    def excluir_lancamento(self, lancamento_id):
        """Exclui um lançamento"""
        if messagebox.askyesno("Confirmar", "Deseja realmente excluir este lançamento?"):
            self.controle.excluir(lancamento_id)
            self.atualizar_dashboard()
    
    def excluir_parcelamento(self, grupo_id):
        """Exclui um parcelamento completo"""
        if messagebox.askyesno("Confirmar", "Deseja excluir TODAS as parcelas deste parcelamento?"):
            self.controle.excluir_grupo_parcelamento(grupo_id)
            self.atualizar_dashboard()
            messagebox.showinfo("Sucesso", "Parcelamento excluído com sucesso!")
    
    def excluir_conta_fixa(self, conta_id):
        """Exclui uma conta fixa"""
        if messagebox.askyesno("Confirmar", "Deseja excluir esta conta fixa e todos os lançamentos associados?"):
            self.controle.excluir_conta_fixa(conta_id)
            self.atualizar_dashboard()
            messagebox.showinfo("Sucesso", "Conta fixa excluída com sucesso!")


def main():
    """Função principal"""
    app = ControleFinanceiroApp()
    app.mainloop()


if __name__ == "__main__":
    main()

