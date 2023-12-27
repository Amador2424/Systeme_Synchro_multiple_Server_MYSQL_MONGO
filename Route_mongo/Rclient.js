const Client = require("../models/Client");
const express = require("express");
const axios = require("axios");
const router = express.Router();

async function createClientMYSQL(nom, prenom, email, id) {
  const client = new Client({ nom, prenom, email, id });
  await client.save();
  console.log("Client créé grace a mysql :", client);
  return client;
}

router.put("/update-client", async (req, res) => {
  const { email, id_mysql } = req.body;
  try {
    const result = await Client.findOneAndUpdate(
      { email: email },
      { id_mysql: id_mysql },
      { new: true }
    );
    if (result) {
      res.status(200).json({ message: "Client mis à jour avec succès" });
    } else {
      res.status(404).json({ message: "Client non trouvé" });
    }
  } catch (error) {
    res
      .status(500)
      .json({ message: "Erreur lors de la mise à jour", error: error.message });
  }
});
router.get("/id/:email", async (req, res) => {
  try {
    const email = req.params.email;
    const client = await Client.findOne({ email: email });

    if (client) {
      res.status(200).send({ id: client._id });
    } else {
      res.status(404).send({ message: "Client non trouvé" });
    }
  } catch (error) {
    res.status(500).send(error);
  }
});

async function createClient(nom, prenom, email) {
  try {
    const client = new Client({ nom, prenom, email });
    await client.save();
    return { message: "Client créé", id: client._id };
  } catch (error) {
    return { error: error.message };
  }
}

router.post("/client", async (req, res) => {
  const result = await createClient(
    req.body.nom,
    req.body.prenom,
    req.body.email
  );
  if (result.error) {
    res.status(500).json(result);
  } else {
    res.status(201).json(result);
  }
});
router.post("/nouveau_client_mysql", async (req, res) => {
  try {
    const client = await createClientMYSQL(
      req.body.nom,
      req.body.prenom,
      req.body.email,
      req.body.id
    );
    res.status(201).send(client);
  } catch (error) {
    res.status(500).send(error.message);
  }
});

// Récupérer un client par ID
router.get("/voir_Un_client/:id", async (req, res) => {
  try {
    const client = await Client.findById(req.params.id);
    if (!client) {
      return res.status(404).send();
    }
    res.send(client);
  } catch (error) {
    res.status(500).send(error);
  }
});

// Mettre à jour un client
router.patch("/MAJclient/:id", async (req, res) => {
  try {
    const client = await Client.findByIdAndUpdate(req.params.id, req.body, {
      new: true,
    });
    if (!client) {
      return res.status(404).send();
    }
    res.send(client);
  } catch (error) {
    res.status(400).send(error);
  }
});

// Supprimer un client
router.delete("/dltClient/:email", async (req, res) => {
  try {
    const client = await Client.findOneAndDelete({ email: req.params.email });
    if (!client) {
      return res.status(404).json({ message: "Client non trouvé" });
    }
    res.json({ message: "Client supprimé avec succès" });
  } catch (error) {
    res
      .status(500)
      .json({ message: "Erreur lors de la suppression", error: error.message });
  }
});

router.get("/clients", async (req, res) => {
  try {
    const clients = await Client.find({});
    res.json(clients);
  } catch (err) {
    res
      .status(500)
      .send("Erreur lors de la récupération des clients: " + err.message);
  }
});

router.delete("/delete_allClients", async (req, res) => {
  try {
    await Client.deleteMany({});
    res.send("Tous les clients ont été supprimés.");
  } catch (err) {
    res
      .status(500)
      .send("Erreur lors de la suppression des clients: " + err.message);
  }
});

router.put("/mAjClient", async (req, res) => {
  const { email, nom, prenom } = req.body;
  try {
    const result = await Client.findOneAndUpdate(
      { email: email },
      { $set: { nom: nom, prenom: prenom } },
      { new: true }
    );
    if (result) {
      res.status(200).json({ message: "Client mis à jour avec succès" });
    } else {
      res.status(404).json({ message: "Client non trouvé" });
    }
  } catch (error) {
    res
      .status(500)
      .json({ message: "Erreur lors de la mise à jour", error: error.message });
  }
});

router.get("/statut_Con", (req, res) => {
  res.status(200).json({ status: "ok" });
});

router.post("/ajouter_journal", async (req, res) => {
  try {
    const nouvelleEntree = new Journal({
      typeModification: req.body.typeModification,
      clientId: req.body.clientId,
      donnees: req.body.donnees,
    });
    await nouvelleEntree.save();
    res.status(201).json({ message: "Entrée de journal ajoutée" });
  } catch (error) {
    res
      .status(500)
      .json({ message: "Erreur lors de l'ajout", error: error.message });
  }
});

router.get("/obtenir_journal", async (req, res) => {
  try {
    const journal = await Journal.find({});
    res.status(200).json(journal);
  } catch (error) {
    res.status(500).json({
      message: "Erreur lors de la récupération",
      error: error.message,
    });
  }
});

module.exports = router;
