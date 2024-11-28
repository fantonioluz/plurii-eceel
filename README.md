# **FinancePro Dashboard**

Uma aplicação interativa construída com **Streamlit** para análise e visualização de dados financeiros, desenvolvida para uma assistência técnica de aparelhos de refrigeração, linha branca, e outros serviços. O aplicativo permite aos usuários monitorar transações, identificar fornecedores mais rentáveis, e realizar análises financeiras detalhadas.

---

## **Funcionalidades**

- Visualização de transações históricas por banco.
- Análise de rentabilidade por fornecedor.
- Filtros dinâmicos para intervalo de tempo e categorias.
- Gráficos interativos com análise de receitas, despesas e rentabilidade.
- Sistema de navegação organizado por abas: Início, Dashboard, Análise por Bancos, e Histórico de Transações.

---

## **Pré-requisitos**

Certifique-se de que você possui os seguintes softwares instalados:

1. Python 3.8 ou superior
2. Gerenciador de pacotes `pip`
3. (Opcional) Ambiente virtual configurado (`venv` ou `virtualenv`)

---

## **Instalação**

### 1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/plurii-eceel.git
```

### 2. Crie um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as dependências:
```bash
pip install -r requirements.txt
```

---

## **Como configurar e rodar a aplicação**

### **1. Configuração inicial**
Antes de rodar a aplicação, é necessário criar e popular o banco de dados. Para isso, execute o seguinte comando no terminal:
```bash
python src/utils/db_creation.py
```

Esse script criará o banco de dados SQLite (`bank_data_csv.db`) com base nos arquivos de dados localizados no diretório `data/`.

### **2. Rodar a aplicação**
Após a criação do banco de dados, inicie a aplicação com o seguinte comando:
```bash
streamlit run src/app.py
```

### **3. Acesse a aplicação**
Abra o navegador e acesse o link fornecido pelo Streamlit, geralmente `http://localhost:8501`.

---

## **Estrutura do projeto**

```plaintext
├── .streamlit/
│   ├── config.toml          # Configurações do Streamlit
├── data/
│   ├── processed/           # Dados processados
│   ├── raw/                 # Dados brutos
├── notebook/
│   ├── data_processing.ipynb # Notebook de processamento de dados
├── src/
│   ├── app.py                # Arquivo principal da aplicação
│   ├── pages/                # Páginas do Streamlit (multiplas abas)
│   │   ├── home_page.py      # Página inicial
│   │   ├── dashboard_page.py # Página de visualização de dados
│   │   ├── bank_page.py      # Análise por banco
│   │   ├── historic_page.py  # Histórico de transações
│   ├── utils/                # Funções de utilidade
│   │   ├── db_creation.py    # Script para criar/popular o banco de dados
│   │   ├── db_utils.py       # Gerenciamento de banco de dados
│   │   ├── analysis_utils.py # Funções de análise de dados
│   │   ├── visualization_utils.py # Funções para gráficos
│   ├── database/             # Banco de dados SQLite
│   ├── images/               # Imagens usadas na aplicação
├── .gitignore                # Arquivos ignorados pelo Git
├── README.md                 # Documentação do projeto
├── requirements.txt          # Lista de dependências do projeto
```

---

## **Funcionalidades das Páginas**

### **1. Início**
Página inicial com informações básicas e botões de acesso rápido.

### **2. Dashboard**
- Visualização de gráficos financeiros detalhados.
- Filtros interativos para intervalo de tempo e categorias.

### **3. Análise por Bancos**
- Informações separadas por banco.
- Rentabilidade por contas e subcontas específicas.

### **4. Histórico de Transações**
- Registro detalhado das transações realizadas.
- Pesquisa por datas e categorias.

---

## **Contribuição**

Se você deseja contribuir com melhorias no projeto:

1. Faça um fork do repositório.
2. Crie uma branch para sua funcionalidade/correção: `git checkout -b minha-feature`.
3. Commit suas alterações: `git commit -m 'Minha nova funcionalidade'`.
4. Envie suas alterações para o repositório remoto: `git push origin minha-feature`.
5. Abra um Pull Request explicando suas alterações.

---

## **Licença**

Este projeto está sob a licença [MIT](LICENSE). Sinta-se à vontade para utilizá-lo e modificá-lo conforme necessário.
```

---

