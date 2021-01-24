const express = require('express');
const app = express();

// Serves Express Yourself website
app.use(express.static('public'));

const port = process.env.PORT || 4001;

const expressions = [{ "name": "hasan" }];
// seedElements(expressions, 'expressions');

// Get all expressions
app.get('/annotations', (req, res, next) => {
    // console.log(req);
    res.send("/annotations")
});

// Get all expressions
app.get('/expressions/:id', (req, res, next) => {
    const foundExpression = getElementById(req.params.id, expressions);
    if (foundExpression) {
        res.send(foundExpression);
    } else {
        res.status(404).send('Monster not found');
    }
});


// Get all expressions
app.get('/annotations/:id', (req, res, next) => {
    res.send('Hello World!')

});
