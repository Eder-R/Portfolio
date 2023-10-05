const mongoose = require('mongoose')

const Book = mongoose.model('Book', {
  Nome:String,
  Autor: String,
  Genero: String,
  Status: Boolean
})

module.exports = Book