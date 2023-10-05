const mongoose = require('mongoose')

const Person = mongoose.model('Person', {
  Nome:String,
  Sala: String,
  Matricula: Number
})

module.exports = Person