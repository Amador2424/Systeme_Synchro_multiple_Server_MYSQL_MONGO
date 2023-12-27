const mongoose = require("mongoose");

const ProduitSchema = new mongoose.Schema({
  nomProduit: String,
  prix: Number,
  categorie: String,
  id_mysql: { type: String, default: null },
  statut: { type: Number, default: 1 },
});
const Produit = mongoose.model("Produit", ProduitSchema);
module.exports = Produit;
