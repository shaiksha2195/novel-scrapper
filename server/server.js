const express = require('express');
const app = express();
const fs = require('fs');

var db = require('knex')({
    client: 'pg',
    connection: {
      host : '127.0.0.1',
      user : 'shaik',
      password : 'shaik',
      database : 'novels'
    }
  });


app.get('/novel/:link', (req, res) => {
    
    const filepath = 'python/scrapper.py';
    const spawn = require("child_process").spawn;
    const pyprocess = spawn('python',[filepath, req.params.link.toString()]);
    
    pyprocess.stdout.on('data', (data) => {
    const text = data.toString('utf-8');
    console.log(text);
    });
    
    res.send("Adding the Novel!");
});
  
app.get('/get/:link/:chap', (req, res) => {
  let jsonfile = require('./python/novels/' + req.params.link.toString() +'.json');
  let num = parseInt(req.params.chap) - 1;
  try{
    let x = '<h2 class = "title">' + Object.keys(jsonfile)[num] + '</h2>'
            + Object.values(jsonfile)[num];
  
    res.send(x);
  }
  catch{
    res.send("no such novel or chapter!")
  }
});

app.get('/getlist', (req, res) => {
  const folder = '../novels';

  fs.readdir(folder, (err, files) => {
    res.json({"files" : files});
  });
});

app.listen(3000);