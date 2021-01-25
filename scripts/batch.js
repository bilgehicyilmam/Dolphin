var MongoClient = require('mongodb').MongoClient
const assert = require('assert');
/*
 * Requires the MongoDB Node.js Driver
 * https://mongodb.github.io/node-mongodb-native
 */

const agg = [
    {
      '$match': {
        'id': new RegExp('localhost')
      }
    }, {
      '$project': {
        'id': {
          '$split': [
            '$id', '/annotations/'
          ]
        }
      }
    }, {
      '$project': {
        'single': {
          '$arrayElemAt': [
            '$id', 1
          ]
        }, 
        'new_id': {
          '$concat': [
            'https://anntt.herokuapp.com/annotations/', {
              '$arrayElemAt': [
                '$id', 1
              ]
            }
          ]
        }
      }
    }, {
      '$set': {
        'id': '$new_id'
      }
    }
  ];
  
  MongoClient.connect(
    'mongodb+srv://new_user_587:YOURPASS@cluster0.hngug.mongodb.net/',
    { useNewUrlParser: true, useUnifiedTopology: true },
    function(connectErr, client) {
      assert.equal(null, connectErr);
      const coll = client.db('annotations').collection('annotations');
    //   coll.aggregate(agg, (cmdErr, result) => {
    //     assert.equal(null, cmdErr);
        
    //   });
    
    for(i = 1; i <= 500000; i++) {

        //  coll.findOne({id: /localhost/}, function(err, result) {
        //     if (err) throw err;
        //     console.log(result.id);
        //     let string = result.id

        //     var regex = /([^\/]+$)/g;
        //     var matches = string.match(regex);  // creates array from matches
        //     single_id = matches[0]
        //     console.log(i + ' ' + single_id)

        //     let new_id = 'https://attnn.herokuapp.com/annotations/' + single_id

        //     console.log(new_id)

        //   });

        let new_id = 'https://anntt.herokuapp.com/annotations/' + i

        console.log(new_id)

          coll.updateOne({id: /localhost/},
            { $set: { id: new_id } }
         )
        
      
    }

    });