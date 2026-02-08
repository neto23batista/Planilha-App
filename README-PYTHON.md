# 💰 Controle Financeiro Profissional - Python Desktop

Aplicativo desktop completo para gerenciamento financeiro pessoal desenvolvido em Python com interface moderna.

## 🎯 Funcionalidades Completas

### ✨ Interface Moderna
- Design profissional com tema escuro
- Layout responsivo em duas colunas
- Ícones para todas as categorias
- Cores diferenciadas para tipos de transação

### 📊 Sistema de Lançamentos
- **Lançamentos do Mês**: Visualize apenas transações do mês atual
- **Entrada/Saída/Investimento**: Três tipos de movimentações
- **Status de Pagamento**: Paga, Não Paga ou Parcelada
- **Categorias**: 9 categorias pré-configuradas com ícones

### 💳 **PARCELAMENTOS INTELIGENTES**
- **Criação Automática**: Informe o número de parcelas e o sistema cria automaticamente
- **Gestão Completa**: Veja todas as parcelas em uma aba dedicada
- **Acompanhamento**: Barra de progresso e percentual pago
- **Controle Individual**: Marque cada parcela como paga separadamente
- **Valor Distribuído**: Valor total dividido igualmente entre as parcelas

**Exemplo**: Compra de R$ 3.600 em 12x → Cria automaticamente 12 lançamentos de R$ 300 nos próximos 12 meses

### 🔄 **CONTAS FIXAS RECORRENTES**
- **Automáticas**: Marcou como recorrente? Ela repete TODO mês
- **Para Sempre**: Continua até você excluir
- **Exemplos**: Aluguel, assinaturas, contas mensais

### 💼 Dashboard Financeiro
- **Total de Entradas** (verde)
- **Total de Saídas** (vermelho)
- **Total Investido** (azul)
- **Gastos Desnecessários** (laranja)
- **Saldo Disponível** (amarelo)
- **Patrimônio Total** (roxo)
- **Status Financeiro**: Positivo ou Endividado
- **Estatísticas**: % economizado, maior gasto, total de lançamentos, contas não pagas

### 📈 Sistema de Abas
1. **📊 Lançamentos do Mês**: Apenas transações do mês atual
2. **💳 Parcelamentos**: Gestão completa de compras parceladas
3. **🔄 Contas Fixas**: Gerenciar contas recorrentes mensais

### 📂 Análise por Categoria
- Total gasto por categoria
- Percentual de cada categoria
- Ícones visuais

### 💾 Persistência de Dados
- Dados salvos automaticamente em JSON
- Carregamento automático ao iniciar
- Backup fácil (basta copiar os arquivos .json)

## 🚀 Instalação

### Requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

#### **Windows:**
```cmd
# 1. Instalar Python
Baixe em: https://www.python.org/downloads/
⚠️ IMPORTANTE: Marque "Add Python to PATH" durante a instalação!

# 2. Instalar dependências
instalar.bat

# 3. Executar aplicativo
iniciar.bat
```

#### **Linux/Mac:**
```bash
# 1. Verificar se Python está instalado
python3 --version

# 2. Instalar dependências
chmod +x instalar.sh
./instalar.sh

# 3. Executar aplicativo
chmod +x iniciar.sh
./iniciar.sh
```

#### **Manual:**
```bash
pip install -r requirements.txt
python controle_financeiro_completo.py
```

## 📖 Como Usar

### ➕ Adicionar Lançamento Simples
1. Preencha a **Data**
2. Digite a **Descrição**
3. Selecione a **Categoria**
4. Escolha o **Status de Pagamento**
5. Preencha o valor em **Entrada**, **Saída** ou **Investimento**
6. Clique em **Adicionar Lançamento**

### 💳 Adicionar Compra Parcelada
1. Preencha normalmente os dados
2. No campo **Parcelas**, digite o número (ex: 12)
3. No campo **Saída**, coloque o **valor total** (ex: 3600.00)
4. Clique em **Adicionar Lançamento**
5. ✅ O sistema cria automaticamente 12 lançamentos de R$ 300,00 nos próximos 12 meses!

**Dica**: Cada parcela criada terá:
- Valor individual (total ÷ parcelas)
- Data ajustada (mês a mês)
- Status "Não Paga" (você marca como paga quando pagar)
- Identificação (1/12, 2/12, etc.)

### 🔄 Adicionar Conta Fixa Mensal
1. Preencha os dados normalmente
2. Marque ☑️ **Conta Fixa Recorrente**
3. Clique em **Adicionar Lançamento**
4. ✅ A partir de agora, todo mês ela será adicionada automaticamente!

**Exemplos de Contas Fixas**:
- Aluguel
- Condomínio
- Internet
- Academia
- Assinaturas (Netflix, Spotify, etc.)

### ✅ Marcar como Paga
Na aba **📊 Lançamentos do Mês**:
1. Encontre o lançamento
2. Clique no botão **✅ Pagar**
3. O status muda instantaneamente!

### 💳 Gerenciar Parcelamentos
Na aba **💳 Parcelamentos**:
- Veja **todas** as compras parceladas
- Acompanhe o **progresso** (barra visual)
- Veja **valor pago** vs **valor restante**
- **Quantas parcelas pagas** (ex: 5/12 pagas)
- Lista de **todas as parcelas** com datas
- Botão para **excluir tudo** de uma vez

### 🔄 Gerenciar Contas Fixas
Na aba **🔄 Contas Fixas**:
- Veja todas as contas recorrentes cadastradas
- Exclua permanentemente (remove a conta E todos os lançamentos)
- Elas continuarão sendo geradas todo mês até você excluir

### 🗑️ Excluir Lançamentos
- Clique no botão **🗑️ Excluir** ao lado do lançamento
- Confirme a exclusão

## 📂 Estrutura de Arquivos

```
controle_financeiro_completo.py  # Aplicativo principal
dados_financeiros.json           # Todos os lançamentos
contas_fixas.json                # Contas recorrentes
ultimo_mes_contas_fixas.txt      # Controle de geração mensal
requirements.txt                 # Dependências Python
instalar.sh / instalar.bat       # Scripts de instalação
iniciar.sh / iniciar.bat         # Scripts para executar
```

## 💾 Backup de Dados

### Fazer Backup
```bash
# Copie estes 3 arquivos:
cp dados_financeiros.json dados_financeiros_backup.json
cp contas_fixas.json contas_fixas_backup.json
cp ultimo_mes_contas_fixas.txt ultimo_mes_contas_fixas_backup.txt
```

### Restaurar Backup
```bash
cp dados_financeiros_backup.json dados_financeiros.json
cp contas_fixas_backup.json contas_fixas.json
cp ultimo_mes_contas_fixas_backup.txt ultimo_mes_contas_fixas.txt
```

## 🎨 Personalização

### Alterar Tema
No arquivo `controle_financeiro_completo.py`, linha 17:
```python
ctk.set_appearance_mode("dark")  # Opções: "dark", "light", "system"
```

### Adicionar Categorias
No arquivo `controle_financeiro_completo.py`, na classe `ControleFinanceiro`:
```python
self.categorias = {
    'Alimentação': '🍔',
    'Sua Nova Categoria': '🆕',  # Adicione aqui
    # ... outras categorias
}
```

## 🔧 Solução de Problemas

### Erro: Python não encontrado
**Windows:**
1. Baixe Python em python.org
2. Reinstale marcando "Add to PATH"
3. Reinicie o computador

**Linux/Mac:**
```bash
# Instalar Python
sudo apt install python3 python3-pip  # Ubuntu/Debian
brew install python3  # Mac
```

### Erro ao instalar customtkinter
```bash
pip install --upgrade pip
pip install customtkinter pillow matplotlib --break-system-packages
```

### Aplicativo não abre
```bash
# Verificar se todas as dependências estão instaladas
pip list | grep customtkinter
pip list | grep matplotlib

# Reinstalar se necessário
pip install -r requirements.txt --force-reinstall
```

### Dados não salvam
- Verifique se tem permissão de escrita na pasta
- Tente executar como administrador
- Verifique se os arquivos .json não estão corrompidos

## 📝 Dicas de Uso

### 🎯 Organize suas Finanças

**1. Configure Contas Fixas Primeiro**
- Aluguel, condomínio, internet, etc.
- Marque como "Conta Fixa Recorrente"
- Todo mês elas aparecem automaticamente!

**2. Use Parcelamentos Corretamente**
- Para compras no cartão parceladas
- Para financiamentos
- O sistema cuida de tudo automaticamente!

**3. Marque Gastos Desnecessários**
- Ajuda a identificar onde cortar gastos
- Acompanhe o total no dashboard

**4. Revise Mensalmente**
- Vá na aba "Lançamentos do Mês"
- Veja apenas o que importa agora
- Marque como pago conforme vai pagando

**5. Acompanhe Parcelamentos**
- Aba dedicada mostra tudo em um lugar
- Veja quanto falta pagar
- Progresso visual facilita o controle

### 💡 Casos de Uso

**Exemplo 1: Compra Parcelada**
```
Descrição: Smart TV 55"
Categoria: Outros
Saída: R$ 2.400,00
Parcelas: 12
Status: Não Paga

Resultado: 12 parcelas de R$ 200,00 criadas automaticamente!
```

**Exemplo 2: Conta Fixa**
```
Descrição: Aluguel
Categoria: Moradia
Saída: R$ 1.500,00
☑️ Conta Fixa Recorrente

Resultado: Todo mês aparece automaticamente!
```

**Exemplo 3: Investimento Mensal**
```
Descrição: Tesouro Direto
Categoria: Investimentos
Investimento: R$ 500,00
☑️ Conta Fixa Recorrente

Resultado: Todo mês você investe automaticamente!
```

## 📊 Diferenças: HTML vs Python

| Recurso | HTML (Browser) | Python (Desktop) |
|---------|----------------|------------------|
| **Instalação** | Nenhuma | Necessário Python |
| **Performance** | Boa | Excelente |
| **Interface** | Web-like | Nativa do sistema |
| **Dados** | localStorage | Arquivos JSON |
| **Portabilidade** | Qualquer navegador | Qualquer SO com Python |
| **Offline** | ✅ | ✅ |
| **Gráficos** | Chart.js | Matplotlib |

## 🤝 Suporte

Para problemas:
1. Verifique se Python está instalado corretamente
2. Confirme que todas as dependências foram instaladas
3. Verifique permissões de leitura/escrita na pasta
4. Tente executar manualmente: `python controle_financeiro_completo.py`

## 📄 Licença

Este aplicativo é de uso livre para fins pessoais.

---

**💙 Desenvolvido em Python com CustomTkinter**

**Versão**: 2.0 - Completa com Parcelamentos e Contas Fixas
