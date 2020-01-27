
const router = require('express').Router();
const shapes = require("../../controllers/shapes.js");

router.get("/", (req, res) => {
  shapes.getAllShapes(req, (status, data = "ok") => res.status(status).send(data));
});

router.get("/:id", (req, res) => {
  shapes.getShapeById(req, (status, data = "ok") => res.status(status).send(data));
});

module.exports = router;