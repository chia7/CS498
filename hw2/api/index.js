const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');


var conn = mysql.createConnection({
	host: '127.0.0.1',
	user: 'replica1',
	password: 'replica1',
	database: 'replica1'
});
conn.connect();


const app = express();
app.use(bodyParser.json());


app.get('/greeting', function (req, res) {
    res.send("Hello World!")
})
app.post('/register', function (req, res) {
  if(Object.keys(req.body).length === 0 || !req.body.username) {
    return res.send("Please provide username");
  }
  let sql = `INSERT INTO Users VALUES('` + req.body.username + `')`;
  conn.query(sql, function (err, result, fields) {
    if (err) throw err;
    res.sendStatus(200);
  });
})
app.get('/list', function (req, res) {
  let sql = `SELECT * FROM Users`;
  conn.query(sql, function (err, result, fields) {
    if (err) throw err;
    var data = {
      users: []
    }
    for (var i = 0; i < result.length; i++) {
      data.users.push(result[i].Username);
    }
    res.send(data);
  });
})
app.post('/clear', function (req, res) {
  let sql = `DELETE FROM Users`;
  conn.query(sql, function (err, result, fields) {
    if (err) throw err;
    res.sendStatus(200);
  });
})

var http = require('http').Server(app);

const PORT = 80;
http.listen(PORT, function() {
	console.log('listening')
});


// app.use(express.urlencoded({
//    extended: false
// }))