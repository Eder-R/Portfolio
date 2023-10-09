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
});
/*FIM DE UM, INICIO DE OUTRO*/

//Prox pagina
$(document).ready(function () {
    var currentPage = 1; // Página atual
    var booksPerPage = 1000; // Livros por página

    // Função para atualizar a exibição da lista de livros com base na página atual
    function updateBookList() {
        console.log("updateBookList chamado. Página atual: " + currentPage);

        var books = $(".livro-container tbody tr");
        var startIndex = (currentPage - 1) * booksPerPage;
        var endIndex = startIndex + booksPerPage;

        console.log("Total de livros: " + books.length);
        console.log("Início: " + startIndex);
        console.log("Fim: " + endIndex);

        // Ocultar todas as linhas de livros
        books.hide();

        // Exibir apenas as linhas da página atual
        books.slice(startIndex, endIndex).show();

        console.log("updateBookList concluído.");
    }


    // Evento de clique no botão "Página Anterior"
    $("#prev-page").click(function () {
        console.log("Botão 'Página Anterior' clicado.")
        if (currentPage > 1) {
            currentPage--;
            updateBookList();
        }
    });

    // Evento de clique no botão "Próxima Página"
    $("#next-page").click(function () {
        console.log("Botão 'Próxima Página' clicado.");
        var totalBooks = $(".livro-container tbody tr").length;
        var totalPages = Math.ceil(totalBooks / booksPerPage);

        if (currentPage < totalPages) {
            currentPage++;
            updateBookList();
        }
    });

    // Inicialmente, atualize a lista de livros para mostrar a primeira página
    updateBookList();
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
