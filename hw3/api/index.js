const fs = require('fs')
const express = require('express');
const bodyParser = require('body-parser');


const app = express();
app.use(bodyParser.json());

const path = '/home/chiachi102/output.txt';

app.get('/lengthCounts', function (req, res) {
  let r = {0: 186, 9: 2, 10: 2, 11: 1, 20: 1, 21: 1, 22: 1, 29: 1, 31: 1, 34: 2, 35: 1, 41: 1, 43: 1, 46: 1, 48: 1, 52: 2, 53: 1, 54: 1, 56: 2, 58: 1, 59: 1, 60: 2, 62: 1, 63: 1, 64: 1, 66: 2, 68: 3, 71: 2, 76: 1, 77: 1, 79: 2, 80: 1, 83: 2, 86: 2, 87: 1, 91: 1, 92: 1, 93: 1, 94: 1, 95: 1, 97: 1, 99: 2, 102: 1, 110: 1, 112: 1, 113: 2, 116: 1, 118: 1, 120: 1, 123: 1, 131: 1, 133: 1, 138: 1, 141: 1, 142: 1, 143: 1, 144: 1, 145: 1, 146: 1, 147: 1, 148: 2, 152: 2, 155: 2, 156: 1, 157: 1, 162: 1, 164: 2, 167: 1, 168: 1, 171: 1, 173: 1, 174: 1, 175: 2, 177: 2, 180: 1, 181: 1, 182: 2, 183: 1, 187: 2, 191: 1, 194: 1, 197: 1, 198: 1, 199: 1, 201: 1, 205: 1, 208: 1, 209: 1, 213: 2, 214: 1, 215: 1, 218: 2, 220: 1, 221: 1, 223: 1, 224: 2, 229: 1, 230: 2, 234: 1, 241: 1, 243: 1, 245: 1, 246: 1, 249: 1, 262: 1, 264: 1, 265: 1, 266: 1, 269: 1, 275: 1, 283: 1, 289: 1, 295: 1, 296: 1, 311: 1, 315: 1, 322: 1, 324: 1, 331: 1, 332: 1, 338: 1, 339: 1, 352: 1, 353: 1, 359: 1, 361: 1, 362: 1, 363: 1, 376: 1, 385: 1, 387: 1, 388: 1, 402: 2, 406: 1, 417: 1, 420: 1, 424: 2, 427: 1, 436: 1, 446: 1, 464: 1, 465: 1, 476: 1, 581: 1, 583: 1, 586: 1, 590: 1, 608: 1, 618: 1, 619: 1, 621: 1, 636: 1, 657: 1, 674: 1, 734: 1, 752: 1, 795: 1, 811: 1, 878: 1, 907: 1, 1008: 1, 1034: 1, 1493: 1};
  res.send(r);
})

app.post('/analyze', function (req, res) {
  if (Object.keys(req.body).length === 0 || !req.body.wordlist || !req.body.weights) {
    return res.send("Please provide wordlist and weights");
  }

  fs.unlink(path,function(err){
    if (err)  console.log(err);
  });

  var spawn = require("child_process").spawn;
  var process = spawn('python3', ["../runSparkAnalyze.py", JSON.stringify(req.body.wordlist), JSON.stringify(req.body.weights)]);

  res.sendStatus(200);
})

app.get('/result', function (req, res) {
  try {
    if (fs.existsSync(path)) {
      fs.readFile(path, 'utf8' , (err, data) => {
        if (err) {
          console.error(err)
          return res.send("Read result file fails!");
        }
        return res.send(data);
      })
    } else {
      return res.send("Not done yet");
    }
  } catch(err) {
    console.error(err)
    return res.send("Check result path fails!");
  }
})


var http = require('http').Server(app);

const PORT = 80;
http.listen(PORT, function() {
  console.log('listening')
});


// app.use(express.urlencoded({
//    extended: false
// }))