const express = require('./server');
const app = express();

let db;
let collection;
var MongoClient = require('mongodb').MongoClient

const mongo_uri = "mongodb+srv://new_user_587:nXxoVnTlNcva3Mro@cluster0.hngug.mongodb.net"

MongoClient
  .connect(mongo_uri, { useNewUrlParser: true, poolSize: 10 })
  .then(client => {
    db = client.db('annotations');
    collection = db.collection('annotations');

    collection.findOne({}, function (err, result) {
            if (err) throw err
        
            console.log(result)
    })

    app.listen(port, () => {
                  console.log(`listening on port ${port}`)
              })
    
  })
  .catch(error => console.error(error));

