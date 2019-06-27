const express = require('express');
const app = express();

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
    const pyprocess = spawn('python',[filepath, 'mr-fu-i-really-love-you', '15', '-l']);
    
    let fin;
    
    pyprocess.stdout.on('data', (data) => {
    const text = data.toString('utf-8');
    fin = JSON.parse(text);
    res.send(fin);
    });
});
   

app.listen(3000);