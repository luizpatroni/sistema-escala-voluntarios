# Sistema de Apoio à Organização de Escalas de Voluntários

## Projeto Integrador II - Tecnologia da Informação

### Descrição

O Sistema de Apoio à Organização de Escalas de Voluntários foi desenvolvido com o objetivo de auxiliar comunidades religiosas na organização e distribuição de voluntários para celebrações e eventos. A aplicação automatiza um processo que normalmente é realizado manualmente, reduzindo erros e facilitando a elaboração das escalas mensais.

O sistema permite o cadastro de voluntários, edição e exclusão de registros, definição de relacionamentos entre participantes (casais, noivos ou namorados) e geração automática de escalas, considerando regras de negócio específicas da comunidade.

---

## Objetivo

Desenvolver uma aplicação web capaz de apoiar a gestão de voluntários e a elaboração de escalas de serviço, utilizando banco de dados relacional, interface web e boas práticas de desenvolvimento de software.

---

## Tecnologias Utilizadas

* Python 3
* Flask
* SQLite
* HTML5
* Jinja2
* Git
* GitHub

---

## Funcionalidades

### Gerenciamento de Voluntários

* Cadastro de voluntários
* Edição de informações cadastradas
* Exclusão de registros
* Associação de parceiros (casais, noivos ou namorados)

### Gerenciamento de Escalas

* Geração automática de escala mensal
* Distribuição dos voluntários entre os domingos do mês
* Manutenção de parceiros na mesma celebração
* Reutilização automática dos voluntários quando necessário

### Banco de Dados

* Modelagem relacional com três tabelas:

  * Voluntários
  * Celebrações
  * Escalas
* Relacionamentos por chaves estrangeiras
* Operações CRUD completas (Create, Read, Update e Delete)

---

## Modelagem do Banco de Dados

### Tabela Voluntários

| Campo       | Tipo    |
| ----------- | ------- |
| id          | INTEGER |
| nome        | TEXT    |
| telefone    | TEXT    |
| parceiro_id | INTEGER |

### Tabela Celebrações

| Campo     | Tipo    |
| --------- | ------- |
| id        | INTEGER |
| data      | TEXT    |
| descricao | TEXT    |

### Tabela Escalas

| Campo         | Tipo    |
| ------------- | ------- |
| id            | INTEGER |
| voluntario_id | INTEGER |
| celebracao_id | INTEGER |
| funcao        | TEXT    |

### Relacionamentos

```text
VOLUNTARIOS
      |
      | 1:N
      |
ESCALAS
      |
      | N:1
      |
CELEBRACOES
```

---

## Operações SQL Implementadas

### Inserção (INSERT)

```sql
INSERT INTO voluntarios(nome, telefone)
VALUES ('Bruna', '99999-9999');
```

### Consulta (SELECT)

```sql
SELECT * FROM voluntarios;
```

### Atualização (UPDATE)

```sql
UPDATE voluntarios
SET telefone = '98888-8888'
WHERE id = 1;
```

### Exclusão (DELETE)

```sql
DELETE FROM voluntarios
WHERE id = 1;
```

---

## Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/luizpatroni/sistema-escala-voluntarios.git
```

### 2. Acessar a pasta do projeto

```bash
cd sistema-escala-voluntarios
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação

```bash
python app.py
```

### 5. Acessar no navegador

```text
http://127.0.0.1:5000
```

---

## Estrutura do Projeto

```text
sistema-escala-voluntarios
│
├── app.py
├── escala.db
├── requirements.txt
├── README.md
├── .gitignore
│
└── templates
    ├── index.html
    ├── editar.html
    └── escala.html
```

---

## Controle de Versão

O desenvolvimento do projeto foi realizado utilizando Git para controle de versão e GitHub para hospedagem do código-fonte. Foram utilizados commits frequentes para registrar as evoluções da aplicação, incluindo a implementação das funcionalidades de cadastro, edição, exclusão de voluntários e geração automática de escalas.

Repositório:

https://github.com/luizpatroni/sistema-escala-voluntarios

---

## Possíveis Melhorias Futuras

* Controle de disponibilidade dos voluntários
* Cadastro de diferentes funções litúrgicas
* Geração de relatórios em PDF
* Interface responsiva com Bootstrap
* Autenticação de usuários
* Dashboard administrativo

---

## Autor

**Luiz Guilherme Patroni Duarte da Silva**

Curso: Tecnologia da Informação

Universidade Federal de Mato Grosso do Sul (UFMS)

Projeto Integrador II – 2026.1
