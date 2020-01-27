const mongodbConnection = require("../dbconfig/connection.js");
const trips = {
  getAllTrips: (req, cb) => {
    const resultsPerPage = 100;
    const collection = mongodbConnection.db().collection("trips");
    const page = parseInt(req.query.page);
    if(page && Number.isInteger(page)){
      collection.find({}, { projection: { _id: 0 } }).limit(resultsPerPage).skip((resultsPerPage * page) - resultsPerPage).toArray((err, result) => {
        if (!err) {
          cb(200, result);
        } else {
          console.log(err);
          cb(500, err);
        }
      });
    } else {
      collection.find({}, { projection: { _id: 0 } }).toArray((err, result) => {
        if (!err) {
          cb(200, result);
        } else {
          console.log(err);
          cb(500, err);
        }
      });
    }
  }
};

module.exports = trips;
