require('dotenv').config()
const express = require('express')
const { default: mongoose } = require('mongoose')
const Book = require('./models/Books')
const bookRoutes = require('./routes/bookRoutes')

const url = process.env.URL

const app = express()

app.use(
  express.json(),
  express.urlencoded({
    extended:true,
  }),
)

app.use('/livros', bookRoutes)
app.get('/', (req, res) => {
  res.json({
    message: 'Olá Express!'
  })
})


mongoose
  .connect(url)
  .then(client => {
  console.log("Sucesso ao se conectar ao banco!")
  app.listen(3000)
  })
  .catch(err => {
  console.log("Erro de conexão!", err)
  })

