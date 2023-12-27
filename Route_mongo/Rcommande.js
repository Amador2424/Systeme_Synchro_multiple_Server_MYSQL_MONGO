const Commande = require("../models/Commande");
const express = require("express");
const router = express.Router();

async function createCommande(clientId, dateCommande, total, produitsIds) {
  const commande = new Commande({
    client: clientId,
    dateCommande,
    total,
    produits: produitsIds,
  });
  await commande.save();
  console.log("Commande créée :", commande);
  return commande;
}

router.post("/nouvelle_commande", async (req, res) => {
  try {
    const commande = await createCommande(
      req.body.clientId,
      req.body.dateCommande,
      req.body.total,
      req.body.produitsIds
    );
    res.status(201).send(commande);
  } catch (error) {
    res.status(500).send(error.message);
  }
});

module.exports = router;
