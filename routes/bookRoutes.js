const router = require('express').Router()
const Book = require('../models/Books')

//CREATE
router.post('/books', async (req, res)=>{
  const {Nome, Autor, Genero} = req.body
  if(!Nome) {
    res.status(422).json({error:"Obrigatório o Nome do livro!"})
  }
  const book = {
    Nome,
    Autor,
    Genero
  }
  try {
    await Book.create(book)

    res.status(201).json({message: 'Livro cadastrado com sucesso!'})
    
  } catch (error) {
    res.status(500).json({error: error})
  }

})

//READ
//findAll
router.get('/books', async (req, res) =>{
  try {
    const book = await Book.find()

    res.status(200).json({book})

  } catch (error) {
    res.status(500).json({error: error})
  }
})
//findOne
router.get('/books/:id', async (req, res) =>{
  try {
    const id = req.params.id
    const book = await Book.findOne({ _id: id })

    if(!book) {
      res.status(422).json({message: "Livro não encontrado"})
    }

    res.status(200).json({book})

  } catch (error) {
    res.status(500).json({error: error})
  }
})

//UPDATE
//DELETE

module.exports = router