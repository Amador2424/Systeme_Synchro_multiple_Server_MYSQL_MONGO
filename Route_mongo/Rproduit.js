const Produit = require("../models/Produit");
const express = require("express");
const router = express.Router();

async function createProduit(nomProduit, prix, categorie) {
  const produit = new Produit({ nomProduit, prix, categorie });
  await produit.save();
  console.log("Produit créé :", produit);
  return produit;
}

router.post("/nouveau_produit", async (req, res) => {
  try {
    const produit = await createProduit(
      req.body.nomProduit,
      req.body.prix,
      req.body.categorie
    );
    res.status(201).send(produit);
  } catch (error) {
    res.status(500).send(error.message);
  }
});

module.exports = router;
