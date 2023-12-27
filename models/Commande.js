const mongoose = require("mongoose");
const CommandeSchema = new mongoose.Schema({
  client: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "Client",
  },
  dateCommande: Date,
  total: Number,
  produits: [
    {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Produit",
    },
  ],
});
const Commande = mongoose.model("Commande", CommandeSchema);

module.exports = Commande;
