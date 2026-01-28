# 💰 Controle Financeiro Profissional

Aplicativo desktop profissional para gerenciamento de finanças pessoais desenvolvido em Python.

## 🎯 Funcionalidades

### ✨ Interface Moderna
- Design profissional com tema escuro
- Interface responsiva e intuitiva
- Ícones para cada categoria
- Cores diferenciadas para entradas, saídas e investimentos

### 📊 Gerenciamento Completo
- **Lançamentos**: Adicione entradas, saídas e investimentos
- **Categorias**: 9 categorias pré-configuradas com ícones
- **Gastos Desnecessários**: Marque gastos que podem ser evitados
- **Histórico**: Visualize todos os lançamentos em tabela interativa

### 💼 Dashboard Financeiro
- **Total de Entradas** (verde)
- **Total de Saídas** (vermelho)
- **Total Investido** (azul)
- **Gastos Desnecessários** (laranja)
- **Saldo Disponível** (amarelo)
- **Patrimônio Total** (roxo)
- **Status**: Indicador de situação financeira (Positivo/Endividado)
- **Estatísticas**: Percentual economizado, maior gasto, total de lançamentos

### 📈 Análise Visual
- **Gráfico de Pizza**: Distribuição de gastos por categoria
- **Lista de Categorias**: Total gasto, percentual e quantidade de lançamentos por categoria

### 💾 Persistência de Dados
- Todos os dados são salvos automaticamente em arquivo JSON
- Os dados são carregados automaticamente ao abrir o aplicativo

## 🚀 Instalação

### Requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

#### Linux/Mac:
```bash
# 1. Instalar dependências
chmod +x instalar.sh
./instalar.sh

# OU manualmente:
pip install -r requirements.txt

# 2. Executar o aplicativo
python controle_financeiro_app.py
```

#### Windows:
```cmd
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar o aplicativo
python controle_financeiro_app.py
```

## 📖 Como Usar

### Adicionar Lançamento
1. Preencha a **Data** (formato: AAAA-MM-DD)
2. Digite a **Descrição** do lançamento
3. Selecione a **Categoria**
4. Preencha o valor em:
   - **Entrada**: Para receitas/salários
   - **Saída**: Para despesas
   - **Investimento**: Para aplicações financeiras
5. Marque **Gasto Desnecessário** se aplicável
6. Clique em **Adicionar Lançamento**

### Excluir Lançamento
1. Selecione o lançamento na tabela
2. Clique em **Excluir Selecionado**
3. Confirme a exclusão

### Visualizar Análises
- O **Dashboard** é atualizado automaticamente
- O **Gráfico de Pizza** mostra a distribuição de gastos
- A **Lista de Categorias** exibe detalhes por categoria

## 📂 Categorias Disponíveis

- 🍔 **Alimentação**: Supermercado, restaurantes, delivery
- 🏠 **Moradia**: Aluguel, condomínio, reformas
- 🚗 **Transporte**: Combustível, transporte público, manutenção
- 🎮 **Lazer**: Cinema, jogos, hobbies
- 💊 **Saúde**: Farmácia, consultas, exames
- 📄 **Contas Fixas**: Luz, água, internet, telefone
- 📈 **Investimentos**: CDB, ações, tesouro direto
- 💼 **Renda**: Salário, freelance, comissões
- 🛍️ **Outros**: Outras despesas

## 💾 Armazenamento de Dados

Os dados são salvos automaticamente no arquivo `dados_financeiros.json` no mesmo diretório do aplicativo.

### Backup Manual
Para fazer backup dos seus dados, basta copiar o arquivo:
```bash
cp dados_financeiros.json dados_financeiros_backup.json
```

### Restaurar Backup
```bash
cp dados_financeiros_backup.json dados_financeiros.json
```

## 🎨 Personalização

### Alterar Tema
No arquivo `controle_financeiro_app.py`, linha 17:
```python
ctk.set_appearance_mode("dark")  # Opções: "dark", "light", "system"
```

### Adicionar Categorias
No arquivo `controle_financeiro_app.py`, na classe `ControleFinanceiro`, método `__init__`:
```python
self.categorias = [
    {"icon": "🆕", "nome": "Nova Categoria"},
    # ... outras categorias
]
```

## 🔧 Solução de Problemas

### Erro ao iniciar o aplicativo
```bash
# Reinstalar dependências
pip install --upgrade customtkinter pillow matplotlib
```

### Gráficos não aparecem
```bash
# Instalar backend do matplotlib
pip install --upgrade matplotlib
```

### Arquivo de dados corrompido
```bash
# Renomear ou excluir o arquivo
mv dados_financeiros.json dados_financeiros_old.json
# O aplicativo criará um novo arquivo ao iniciar
```

## 📝 Dicas de Uso

1. **Organize suas categorias**: Use categorias específicas para facilitar a análise
2. **Marque gastos desnecessários**: Ajuda a identificar onde economizar
3. **Registre investimentos**: Acompanhe o crescimento do seu patrimônio
4. **Faça backups regulares**: Proteja seus dados financeiros
5. **Revise periodicamente**: Analise os gráficos mensalmente

## 🤝 Suporte

Para dúvidas ou problemas, verifique:
- Se todas as dependências estão instaladas corretamente
- Se o Python está atualizado (versão 3.8+)
- Se o arquivo `dados_financeiros.json` não está corrompido

## 📄 Licença

Este aplicativo é de uso livre para fins pessoais.

---

**Desenvolvido com 💙 usando Python e CustomTkinter**
