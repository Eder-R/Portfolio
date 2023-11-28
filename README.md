# LibManager

## Indice

- [LibManager](#libmanager)
  - [Indice](#indice)
  - [Definição do problema](#definição-do-problema)
  - [Requisitos](#requisitos)
  - [Caso de Uso](#caso-de-uso)
    - [**Atores:**](#atores)
    - [**Casos de Uso:**](#casos-de-uso)
  - [Quadro Kambam](#quadro-kambam)

## Definição do problema

O problema com o gerenciamento atual da biblioteca de uma pequena escola é que ele não é eficiente. O sistema atual é baseado em planilhas e e-mails, o que torna difícil acompanhar os livros e outros materiais. Isso pode levar a problemas como livros perdidos ou danificados, multas não pagas e alunos que não conseguem encontrar os livros que precisam.

Uma solução que foi encontrada para esse problema é criar um sistema web. Esse sistema permitiria aos alunos e professores pesquisar livros, verificar livros, pagar multas e muito mais. O sistema também poderia ser usado para gerar relatórios sobre o uso da biblioteca, o que ajudaria a escola a tomar decisões sobre quais livros comprar e como alocar recursos.

O sistema web, seria uma solução eficiente para o problema. O sistema seria fácil de usar e manter, e ajudaria a escola a economizar tempo e dinheiro.

Aqui estão algumas das vantagens de usar um sistema web, para gerenciar uma biblioteca escolar:

- O sistema será fácil de usar e manter.
- O sistema ajudará a escola a economizar tempo e dinheiro.
- O sistema permitirá aos alunos e professores pesquisar livros, verificar livros, pagar multas e muito mais.
- O sistema poderá ser usado para gerar relatórios sobre o uso da biblioteca, o que ajudaria a escola a tomar decisões sobre quais livros comprar e como alocar recursos.


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

## Caso de Uso

![Caso de Uso](assets/images/Caso%20de%20Uso.svg)

### **Atores:**

1. **Usuário (Aluno/Professor/Funcionário):** Pessoas que utilizam o sistema para buscar, reservar e emprestar livros.

2. **Bibliotecário:** Responsável pela administração do sistema, incluindo cadastro de livros, gerenciamento de empréstimos, devoluções e geração de relatórios.

---

### **Casos de Uso:**

1. **Pesquisar Livros:**
   - **Ator Principal:** Usuário
   - **Descrição:** O usuário pode pesquisar livros no catálogo da biblioteca com base em critérios como título, autor, categoria, ISBN, etc.

2. **Realizar Empréstimo:**
   - **Ator Principal:** Usuário
   - **Descrição:** O usuário pode solicitar empréstimo de livros disponíveis na biblioteca. O sistema registra o empréstimo e gera um recibo.

3. **Realizar Devolução:**
   - **Ator Principal:** Usuário
   - **Descrição:** O usuário pode devolver os livros emprestados. O sistema atualiza o status do livro e calcula multas, se aplicável.

4. **Reservar Livro:**
   - **Ator Principal:** Usuário
   - **Descrição:** O usuário pode reservar um livro que está atualmente emprestado por outro usuário. O sistema notifica o usuário quando o livro estiver disponível.

5. **Cadastrar Livro:**
   - **Ator Principal:** Bibliotecário
   - **Descrição:** O bibliotecário pode cadastrar novos livros no sistema, incluindo informações como título, autor, ISBN, etc.

6. **Gerar Relatórios:**
   - **Ator Principal:** Bibliotecário
   - **Descrição:** O bibliotecário pode gerar relatórios sobre o uso da biblioteca, como os livros mais emprestados, frequência de empréstimos, multas, etc.

7. **Configurar Sistema:**
   - **Ator Principal:** Bibliotecário
   - **Descrição:** O bibliotecário pode personalizar as configurações do sistema, como prazos de empréstimo, políticas de multas, etc.

8. **Autenticar Usuário:**
   - **Ator Principal:** Sistema
   - **Descrição:** O sistema autentica os usuários (alunos, professores, funcionários) para acessar funcionalidades restritas.

## Quadro Kambam

[Clique aqui para acessar o quadro Kambam](https://trello.com/invite/b/Ung8zIbd/ATTI4ccbb46809eb1a9209ccd043b5b8db3c1AE3E768/to-do)

---

## ToDo

- [ ] Cadastro de Livros
    - Ver com alguem se conseguimos saber o erro.
- [ ] Cadastro de Clientes
- [ ] CI/ CD
    - Pedir para o ajuda para o Gillbert ajuda com isso.
- [ ] Testes Unitários
    - Pesquisando ainda, ver links compartilhados com Matheus Duarte
- [ ] Consertar o arquivo README.md
    - [ ] Inserir instruções de como utilizar;
    - [ ] Inserir instruções de como contribuir;
    - [ ] Reinserir as imagens dos que se perderam nos processos durante as atualições;
    - [ ] Inserir informações de ajudantes;

## Pesquisar mais a fundo

Testes Unitarios: 
    `https://medium.com/@otaviobn/tdd-com-flask-e-unittest-3f66036a240b`
    
Deploy real do projeto: `https://pythonbasics.org/deploy-flask-app/`, `https://medium.com/swlh/how-to-host-your-flask-app-on-pythonanywhere-for-free-df8486eb6a42`
