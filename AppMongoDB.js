const express = require("express");
const mongoose = require("mongoose");
require("dotenv").config();
const app = express();
app.use(express.json());

const Client = require("./models/Client");
const Commande = require("./models/Commande");
const Produit = require("./models/Produit");
const API_Client = require("./Route_mongo/Rclient");
const API_Produit = require("./Route_mongo/Rproduit");
const API_Commande = require("./Route_mongo/Rcommande");
app.use("/produit", API_Produit);
app.use("/client", API_Client);
app.use("/commande", API_Commande);
mongoose
  .connect(process.env.MONGODB_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => console.log("Connected to MongoDB"))
  .catch((err) => console.error("Could not connect to MongoDB", err));

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Listening on port ${port}...`));
