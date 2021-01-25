const assert = require('assert');
var MongoClient = require('mongodb').MongoClient

MongoClient.connect(
  'mongodb+srv://new_user_587:YOURPASS@cluster0.hngug.mongodb.net/',
  { useNewUrlParser: true, useUnifiedTopology: true },
  function (connectErr, client) {
    assert.equal(null, connectErr);
    const coll = client.db('annotations').collection('annotations');

    for (i = 1; i <= 500000; i++) {
      let new_id = 'https://anntt.herokuapp.com/annotations/' + i
      console.log(new_id)
      coll.updateOne({ id: /localhost/ },
        { $set: { id: new_id } }
      )
    }
  });