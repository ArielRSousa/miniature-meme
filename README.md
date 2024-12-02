# 💰 Gerenciador Financeiro Pessoal

Um aplicativo interativo para ajudar no controle de finanças pessoais. Registre transações de ganhos e gastos, visualize relatórios financeiros e tire dúvidas sobre finanças com um chatbot de IA integrado.

---

## 🚀 Funcionalidades

- **Registro de Transações**: Adicione ganhos e gastos com descrição, valor e data.
- **Resumo Financeiro**:
  - Total de ganhos.
  - Total de gastos.
  - Saldo atual.
- **Filtros Dinâmicos**:
  - Filtre transações por tipo, categoria e intervalo de datas.
- **Relatórios Visuais**:
  - Gráficos de evolução financeira.
  - Distribuição de ganhos e gastos.
- **Chatbot de Finanças**:
  - Tire dúvidas sobre gestão financeira com inteligência artificial.

---

## 📦 Estrutura do Projeto

```plaintext
.
├── app.py                 # Código principal do aplicativo Streamlit
├── data.py                # Manipulação de dados (carregar, salvar, registrar, remover)
├── business_rules.py      # Regras de negócio (validação de saldo e lógica financeira)
├── utils.py               # Funções auxiliares (cálculos e geração de IDs)
├── transacoes.csv         # Base de dados local das transações
├── .env                   # Variáveis de ambiente (API Key)
├── requirements.txt       # Dependências do projeto
└── README.md              # Documentação do projeto

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+**
- **Streamlit**: Framework para criação de aplicativos web interativos.
- **Pandas**: Manipulação e análise de dados financeiros.
- **Plotly**: Geração de gráficos interativos.
- **OpenAI API**: Chatbot de IA para tirar dúvidas financeiras.
- **Python-dotenv**: Gerenciamento de variáveis de ambiente.

---

## 📋 Pré-requisitos

```bash
# Certifique-se de ter Python 3.9+ instalado.
python --version

# Instale as dependências do projeto.
pip install -r requirements.txt
```
# Crie um arquivo dotenv.env no diretório do projeto com o seguinte conteúdo:
OPENAI_API_KEY=sua_chave_aqui

## 🚀 Como Executar o Projeto

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

# Instale as dependências
pip install -r requirements.txt

# Execute o aplicativo Streamlit
streamlit run app.py
```