const mongodbConnection = require("../dbconfig/connection.js");
const trips = {
  getAllRoutes: (req, cb) => {
    const collection = mongodbConnection.db().collection("routes");
    collection.find({}, { projection: { _id: 0 } }).toArray((err, result) => {
      if (!err) {
        cb(200, result);
      } else {
        console.log(err);
        cb(500, err);
      }
    });
  }
};

module.exports = trips;
