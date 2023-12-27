const mongoose = require("mongoose");

const ClientSchema = new mongoose.Schema({
  nom: String,
  prenom: String,
  email: String,
  id_mysql: { type: String, default: null },
});
const Client = mongoose.model("Client", ClientSchema);

module.exports = Client;
