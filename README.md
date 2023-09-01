# LibManager

- [LibManager](#libmanager)
  - [C4](#c4)
    - [1. Contexto (Context)](#1-contexto-context)
    - [2. Container (Contêiner)](#2-container-contêiner)
    - [3. Componente (Component)](#3-componente-component)
    - [4. Código (Code)](#4-código-code)
  - [Requisitos](#requisitos)

## C4

### 1. Contexto (Context)

- **Nome:** LibManager
- **Objetivo:** Fornecer uma solução para gerenciar a coleção de livros de uma biblioteca escolar.
- **Stakeholders:** Bibliotecários, usuários da biblioteca.

---

### 2. Container (Contêiner)

- **Nome:** Aplicação da Biblioteca
  - **Tecnologias:** Programação web: JavaScript (Node.js);

  - **Responsabilidade:** Interface com o usuário, gerenciamento de pedidos, pesquisa de livros.

- **Nome:** Banco de Dados
  - **Tecnologia:** Banco de Dados MongoDB
  - **Responsabilidade:** Armazenamento de informações sobre livros, autores, usuários e transações.

---

### 3. Componente (Component)

- **Nome:** Módulo de Autenticação
  - **Responsabilidade:** Gerenciar autenticação de usuários (login/logout).

- **Nome:** Módulo de Pesquisa
  - **Responsabilidade:** Permitir aos usuários pesquisar livros por título, autor, gênero.

- **Nome:** Módulo de Empréstimo
  - **Responsabilidade:** Permitir aos usuários solicitar empréstimo de livros.

- **Nome:** Módulo de Devolução
  - **Responsabilidade:** Gerenciar a devolução de livros emprestados.

---

### 4. Código (Code)

- **Estrutura de Pacotes:**
  - `lib_manager`
    - `models\auth`: Contém classes relacionadas à autenticação.
    - `models\research`: Contém classes relacionadas à pesquisa de livros.
    - `models\loan`: Contém classes relacionadas ao empréstimo de livros.
    - `models\return`: Contém classes relacionadas à devolução de livros.
    - `models\books`: Contém classes de modelo para representar livros, autores, usuários, etc.
    - `dbConfig`: Contém classes para acesso ao banco de dados.

---

## Requisitos

- **Cadastro de Livros:**
  - Cadastro de informações dos livros, incluindo título, autor, editora, ISBN, ano de publicação, número de exemplares, etc.

- **Cadastro de Usuários:**
  - Cadastro de alunos, professores e funcionários com informações pessoais, número de identificação, etc.

- **Controle de Empréstimos e Devoluções:**
  - Registro de empréstimos de livros para usuários.
  - Data de empréstimo e data de devolução prevista.
  - Geração de recibos de empréstimos.

- **Pesquisa e Catálogo:**
  - Sistema de pesquisa que permite aos usuários buscar livros por título, autor, categoria, ISBN, etc.
  - Exibição de informações detalhadas do livro, incluindo disponibilidade.

- **Reservas de Livros:**
  - Capacidade de reservar livros que estão atualmente emprestados.

- **Relatórios e Estatísticas:**
  - Geração de relatórios sobre o uso da biblioteca, como livros mais emprestados, frequência de empréstimos, etc.

- **Gerenciamento de Estoque:**
  - Controle de estoque de livros, incluindo adição, remoção e atualização de exemplares.

- **Segurança e Autenticação:**
  - Segurança para proteger informações sensíveis dos usuários e garantir que apenas pessoal autorizado tenha acesso ao sistema.

- **Backup e Recuperação de Dados:**
  - Implementação de rotinas de backup para proteger os dados da biblioteca.

- **Suporte Técnico e Treinamento:**
  - Fornecimento de suporte técnico e treinamento para a equipe da biblioteca.
