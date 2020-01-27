const mongodbConnection = require("../dbconfig/connection.js");
const shapes = {
  getAllShapes: (req, cb) => {
    const resultsPerPage = req.query.resultsPerPage ? parseInt(req.query.resultsPerPage) : 100;
    const collection = mongodbConnection.db().collection("shapes");
    const page = req.query.page ? parseInt(req.query.page) : 1;
    if (page && Number.isInteger(page) && Number.isInteger(resultsPerPage)) {
      collection
        .find({}, { projection: { _id: 0 } })
        .limit(resultsPerPage)
        .skip(resultsPerPage * page - resultsPerPage)
        .toArray((err, result) => {
          if (!err) {
            cb(200, result);
          } else {
            console.log(err);
            cb(404, err);
          }
        });
    } else {
      cb(400, err);
    }
  },
  getShapeById: (req, cb) => {
    const collection = mongodbConnection.db().collection("shapes");
    const id = req.params.id;
    if (!isNaN(id)) {
      collection.findOne({shape_id: id}, { projection: { _id: 0 } }).then((result) => {
          cb(200, result);
      })
      .catch(e => {
        cb(404, {error: "There was an finding that shape"});
      })
    } else {
      cb(400, {error: "{id} is required in the path"});
    }
  }
};

module.exports = shapes;
