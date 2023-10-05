const router = require('express').Router()
const Person = require('../models/Persons')

//CREATE
router.post('/person', async (req, res)=>{
  const {Nome, Sala, Matricula} = req.body
  if(!Nome) {
    res.status(422).json({error:"Obrigatório o nome da pessoa!"})
  }
  if(!Matricula) {
    res.status(422).json({error:"Obrigatório a sala da pessoa!"})
  }
  const person = {
    Nome,
    Sala,
    Matricula
  }
  try {
    await Person.create(person)

    res.status(201).json({message: 'Pessoa cadastrada com sucesso!'})
    
  } catch (error) {
    res.status(500).json({error: error})
  }

})

//READ
//findAll
router.get('/person', async (req, res) =>{
  try {
    const person = await Person.find()

    res.status(200).json({person})

  } catch (error) {
    res.status(500).json({error: error})
  }
})
//findOne
router.get('/person/:id', async (req, res) =>{
  try {
    const id = req.params.id
    const person = await Person.findOne({ _id: id })

    if(!person) {
      res.status(422).json({message: "Livro não encontrado"})
    }

    res.status(200).json({person})

  } catch (error) {
    res.status(500).json({error: error})
  }
})

//UPDATE
//DELETE

module.exports = router