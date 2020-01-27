const router = require("express").Router();
const tripsRoute = require('./trips');
const routesRoute = require('./routes');
const shapesRoute = require('./shapes');


router.use('/trips', tripsRoute);
router.use('/routes', routesRoute);
router.use('/shapes', shapesRoute);


module.exports = router;