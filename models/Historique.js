const mongoose = require("mongoose");

const JournalSchema = new mongoose.Schema({
  typeModification: String,
  clientId: mongoose.Schema.Types.ObjectId,
  dateModification: { type: Date, default: Date.now },
});
const Journal = mongoose.model("Journal", JournalSchema);
module.exports = Journal;
