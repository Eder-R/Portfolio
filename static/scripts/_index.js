function cadastrarLivro() {
    var form = $("#product-form");

    form.submit(function onSubmitForm(event) {
        event.preventDefault();

        var formData = form.serialize();

        $.ajax({
            type: "POST",
            url: "/cadastro_livro",
            data: formData,
            success: function onCadastroLivroSuccess(response) {
                console.log(response);
            }
        });
    });

    $("#redirect-button").click(function onRedirectButtonClick() {
        window.location.href = "/cadastro_livros";
    });

    $("#redirect-button-plp").click(function onRedirectButtonClick() {
        window.location.href = "/cadastro_pessoa";
    });
};

function redirectOnSubmit(event) {
    // Impede o envio padrão do formulário
    event.preventDefault();

    // Lógica para salvar os dados do formulário (pode ser feita com AJAX ou submissão normal)

    // Redireciona para a página "/"
    window.location.href = "/";
  }

$(document).ready(function paginacaoLivros() {
    var currentPage = 1;
    var booksPerPage;

    function atualizarListaLivros() {
        var books = $(".livro-container tbody tr");
        var startIndex = (currentPage - 1) * booksPerPage;
        var endIndex = startIndex + booksPerPage;

        books.hide();
        books.slice(startIndex, endIndex).show();
    }

    function obterNumeroLivros() {
        $.ajax({
            url: "/get_books_count",
            method: "GET",
            success: function onGetBooksCountSuccess(data) {
                booksPerPage = data.count;
                atualizarListaLivros();
            }
        });
    }

    obterNumeroLivros();

    $("#prev-page").click(function onPrevPageClick() {
        if (currentPage > 1) {
            currentPage--;
            atualizarListaLivros();
        }
    });

    $("#next-page").click(function onNextPageClick() {
        var books = $(".livro-container tbody tr");
        var totalBooks = books.length;
        var maxPage = Math.ceil(totalBooks / booksPerPage);

        if (currentPage < maxPage) {
            currentPage++;
            atualizarListaLivros();
        }
    });
});

$(document).ready(function obterAutores() {
    $.ajax({
        url: '/get_authors',
        type: 'GET',
        success: function onGetAuthorsSuccess(data) {
            $('#autorSelect').empty();
            $('#autorSelect').append('<option value="">Autor</option>');

            for (var i = 0; i < data.authors.length; i++) {
                $('#autorSelect').append('<option value="' + data.authors[i] + '">' + data.authors[i] + '</option>');
            }
        }
    });
});

$(document).ready(function obterGeneros() {
    $.ajax({
        url: '/get_genres',
        type: 'GET',
        success: function onGetGenresSuccess(data) {
            $('#generoSelect').empty();
            $('#generoSelect').append('<option value="">Gênero</option>');

            for (var i = 0; i < data.genres.length; i++) {
                $('#generoSelect').append('<option value="' + data.genres[i] + '">' + data.genres[i] + '</option>');
            }
        }
    });
});

function edit_book() {
    // Obter os valores do formulário
    var nomeLivro = document.getElementById('nomeLivro').value;
    var autorLivro = document.getElementById('autorLivro').value;
    var generoLivro = document.getElementById('generoLivro').value;
    var statusLivro = document.getElementById('statusLivro').value;

    // Exemplo de dados do livro (id é apenas um exemplo, você precisará obter o ID real do livro)
    var dadosLivro = {
        id: 1, // Substitua pelo ID real do livro
        nome: nomeLivro,
        autor: autorLivro,
        genero: generoLivro,
        status: statusLivro === 'true' // Convertendo para booleano
    };

    // Enviar dados para o servidor Flask usando AJAX
    fetch('/alterar_dados_livro', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(dadosLivro),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Resposta do servidor:', data);
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}