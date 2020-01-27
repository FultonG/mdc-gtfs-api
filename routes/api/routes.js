
const router = require('express').Router();
const routes = require("../../controllers/routes.js");

router.get("/", (req, res) => {
  routes.getAllRoutes(req, (status, data = "ok") => res.status(status).send(data));
});

module.exports = router;