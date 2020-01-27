const express = require("express");
const swaggerUi = require('swagger-ui-express');
const swaggerDocument = require('./swagger.json');
const bodyParser = require("body-parser");
const apiRoutes = require("./routes/api");
const PORT = process.env.PORT || 3001;
const app = express();

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use("/api", apiRoutes);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

app.get("*", function(req, res) {
    res.sendStatus(404);
})

app.listen(PORT, function() {
    console.log(`Server running on port ${PORT}!`);
});