
const router = require('express').Router();
const trips = require("../../controllers/trips.js");

router.get("/", (req, res) => {
  trips.getAllTrips(req, (status, data = "ok") => res.status(status).send(data));
});

module.exports = router;