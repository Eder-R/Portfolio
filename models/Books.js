const { default: mongoose } = require('mongoose')

const Book = mongoose.model('Book', {
  Nome:String,
  Autor: String,
  Genero: String

})

module.exports = Book