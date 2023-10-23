// cadastro_livro.js
$(document).ready(function () {
    var form = $("#product-form");

    form.submit(function (event) {
        event.preventDefault();

        var formData = form.serialize();

        $.ajax({
            type: "POST",
            url: "/cadastro_livro",
            data: formData,
            success: function (response) {
                console.log(response);
            }
        });
    });
    
    // Evento de clique no botão de redirecionamento
    $("#redirect-button").click(function () {
        // Redirecione para a página de cadastro de livros
        window.location.href = "/books"; // Substitua "/cadastro_livros" pela URL da sua página de cadastro de livros
    });
});
/*FIM DE UM, INICIO DE OUTRO*/

//Prox pagina
$(document).ready(function () {
    var currentPage = 1; // Página atual
    var booksPerPage; // Livros por página

    // Função para atualizar a exibição da lista de livros com base na página atual
    function updateBookList() {
        var books = $(".livro-container tbody tr");
        var startIndex = (currentPage - 1) * booksPerPage;
        var endIndex = startIndex + booksPerPage;

        // Ocultar todas as linhas de livros
        books.hide();

        // Exibir apenas as linhas da página atual
        books.slice(startIndex, endIndex).show();
    }

    // Função para buscar o número de livros no banco de dados
    function getBooksCount() {
        $.ajax({
            url: "/get_books_count", // Rota no Flask para buscar a contagem de livros
            method: "GET",
            success: function (data) {
                booksPerPage = data.count;
                updateBookList();
            }
        });
    }

    // Inicialmente, buscar o número de livros e mostrar a primeira página
    getBooksCount();

    // Evento de clique no botão "Página Anterior"
    $("#prev-page").click(function () {
        if (currentPage > 1) {
            currentPage--;
            updateBookList();
        }
    });

    // Evento de clique no botão "Próxima Página"
    $("#next-page").click(function () {
        var books = $(".livro-container tbody tr");
        var totalBooks = books.length;
        var maxPage = Math.ceil(totalBooks / booksPerPage);

        if (currentPage < maxPage) {
            currentPage++;
            updateBookList();
        }
    });
});


/*FIM DE UM, INICIO DE OUTRO*/

$(document).ready(function () {
    $.ajax({
        url: '/get_authors',  // Rota para obter os autores
        type: 'GET',
        success: function (data) {
            $('#autorSelect').empty();  // Limpe as opções atuais
            $('#autorSelect').append('<option value="">Autor</option>');  // Adicione a opção "Todos"

            // Preencha o <select> com os autores recebidos
            for (var i = 0; i < data.authors.length; i++) {
                $('#autorSelect').append('<option value="' + data.authors[i] + '">' + data.authors[i] + '</option>');
            }
        }
    });
});

/*FIM DE UM, INICIO DE OUTRO*/

$(document).ready(function () {
    $.ajax({
        url: '/get_genres',  // Rota para obter os gêneros
        type: 'GET',
        success: function (data) {
            $('#generoSelect').empty();  // Limpe as opções atuais
            $('#generoSelect').append('<option value="">Genero</option>');  // Adicione a opção "Todos"

            // Preencha o <select> com os gêneros recebidos
            for (var i = 0; i < data.genres.length; i++) {
                $('#generoSelect').append('<option value="' + data.genres[i] + '">' + data.genres[i] + '</option>');
            }
        }
    });
});

$(document).ready(function () {
    // Função para buscar a capa do livro com base no nome do livro
    function getBookCover(title) {
        var googleBooksAPI = "https://www.googleapis.com/books/v1/volumes?q=" + title;

        $.ajax({
            type: "GET",
            url: googleBooksAPI,
            success: function (data) {
                // Verifique se há resultados
                if (data.totalItems > 0) {
                    var book = data.items[0].volumeInfo;
                    if (book.imageLinks && book.imageLinks.thumbnail) {
                        // Exiba a capa do livro na página
                        var coverUrl = book.imageLinks.thumbnail;
                        $("#book-cover").attr("src", coverUrl);
                    } else {
                        // Caso a capa não esteja disponível
                        $("#book-cover").attr("src", "../imgs/NotFound.png");
                    }
                } else {
                    // Caso nenhum resultado seja encontrado
                    $("#book-cover").attr("src", "../imgs/NotFound.png");
                }
            },
            error: function () {
                // Trate erros de solicitação aqui
            }
        });
    }

    // Manipule o envio do formulário
    $("#product-form").submit(function (event) {
        event.preventDefault();
        var formData = form.serialize();
        // Obtém o título do livro do campo de entrada
        var bookTitle = $("#book-title").val();
        // Chame a função para buscar a capa do livro
        getBookCover(bookTitle);

        // Continue com a submissão do formulário
        $.ajax({
            type: "POST",
            url: "/cadastro_livro",
            data: formData,
            success: function (response) {
                console.log(response);
            }
        });
    });
});
