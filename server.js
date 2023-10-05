require('dotenv').config()
const express = require('express')
const { MongoClient } = require('mongodb')

const Book = require('./models/Books')
const bookRoutes = require('./routes/bookRoutes')

const Person = require('./models/Persons')
const personRoutes = require('./routes/personRoutes')
const url = process.env.URL

const app = express()

app.use(
  express.json(),
  express.urlencoded({
    extended:true,
  }),
)

app.use('/persons', personRoutes)
app.get('/persons', (req, res) => {
  res.json({
    message: 'Olá Pessoa Express!'
  })
})

app.use('/books', bookRoutes)
app.get('/books', (req, res) => {
  res.json({
    message: 'Olá Livro Express!'
  })
})


MongoClient
  .connect(url)
  .then(() => {
  console.log("Sucesso ao se conectar ao banco!")
  app.listen(3000)
  })
  .catch(err => {
  console.log("Erro de conexão!", err)
  })

