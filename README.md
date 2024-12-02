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
```
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
## Crie um arquivo .env no diretório do projeto com o seguinte conteúdo:
```bash
OPENAI_API_KEY=sua_chave_aqui
```

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

## 📊 Relatórios Disponíveis
1. Resumo Financeiro:
   - Total de ganhos, gastos e saldo atual.

2. Evolução Financeira:
   - Gráfico de linha mostrando a evolução de ganhos e gastos ao longo do tempo.

3. Distribuição de Ganhos e Gastos:
   - Gráfico de pizza com a proporção entre ganhos e gastos.

## 🛡️ Licença
Este trabalho está licenciado sob a Licença Creative Commons Attribution-NonCommercial 4.0 International.
Você pode usar, modificar e compartilhar este projeto apenas para fins não comerciais.

Para mais detalhes, consulte a licença completa:
https://creativecommons.org/licenses/by-nc/4.0/legalcode


## ✨ Autor
Criado por Ariel S. Entre em contato para dúvidas ou colaborações!