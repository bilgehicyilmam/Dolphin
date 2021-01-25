const express = require('express');
const app = express();

// Serves Express Yourself website
app.use(express.static('public'));

const port = process.env.PORT || 4001;

app.get('/', function(req, res){
    res.redirect('/annotations');
 });



/**
 * Returns random 10 annotations
 * @param {number} id
 * @returns {Object}
 */ 
app.get('/annotations', (req, res, next) => {
    let page = 0
    page = parseInt(req.query.page, 10)
    const skip = page * 10
    var query = {};
    collection.find(query).limit(10).skip(skip).toArray(function (err, result) {
        if (err) throw err;
        res.send(result)
    });
});


/**
 * Search annotations that has the keyword 
 * @param {string} keyword
 * @returns {Object}
 */ 
app.get('/annotations/search/:keyword', (req, res, next) => {

    var query = { 'target.selector.exact': req.params.keyword };
    collection.find(query).limit(10).toArray(function (err, result) {
        if (err) throw err;
        if (result.length > 0) {
            res.send(result)
        } else {
            res.send({ 'message': 'Not Found' }).status(204)
        }

    });
});


/*

:param id: an article id  
*/
app.get('/annotations/:id', (req, res, next) => {

    collection.findOne({ id: { $regex: '/' + req.params.id } }, function (err, result) {
        if (err) throw err
        res.send(result)
    })


});

// Get all annotations of an article
app.get('/annotations/pmid/:id', (req, res, next) => {

    collection.find({ 'target.source': { $regex: '/' + req.params.id } }).toArray(function (err, result) {
        if (err) throw err
        res.send(result)
    })


});

// Get all annotations of an article
app.get('/annotations/pmid/:id/label', (req, res, next) => {

    collection.find(
        { 'target.source': { $regex: '/' + req.params.id } },
        { projection: { _id: 0, id: 1, 'target.selector.exact': 1 } })
        .toArray(function (err, result) {
            if (err) throw err
            res.send(result)
        })
});


// Get all annotations of an article
// return: annotations of an article
app.get('/annotations/pmid/:id/target', (req, res, next) => {
    collection.find(
        { 'target.source': { $regex: '/' + req.params.id } },
        { projection: { _id: 0, id: 1, 'target': 1 } })
        .toArray(function (err, result) {
            if (err) throw err
            res.send(result)
        })
});

// db initialization
// pooling
let db;
let collection;
var MongoClient = require('mongodb').MongoClient
const mongo_uri = "mongodb+srv://new_user_587:nXxoVnTlNcva3Mro@cluster0.hngug.mongodb.net"

MongoClient
    .connect(mongo_uri, { useNewUrlParser: true, poolSize: 10, useUnifiedTopology: true })
    .then(client => {
        db = client.db('annotations');
        collection = db.collection('annotations');

        app.listen(port, () => {
            console.log(`listening on port ${port}`)
        })

    })
    .catch(error => console.error(error));
