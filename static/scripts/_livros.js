// cadastro_livro.js
$(document).ready(function() {
  var form = $("#product-form");

  form.submit(function(event) {
      event.preventDefault();

      var formData = form.serialize();

      $.ajax({
          type: "POST",
          url: "/cadastro_livro",
          data: formData,
          success: function(response) {
              console.log(response);
          }
      });
  });
});
