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

let novel = ['zombie-sister-strategy', 'i-alone-level-up'];
let last;

db.select('*').from('novels').where({novel:novel[0]}).then((data) => {
    if(!data[0]){
        db('novels').insert({novel:novel[0], lastchap:0});
        last = 0;
    }
    else{
        last = data[0].lastchap;
    }
    const result = require('./zombie-sister-strategy.json');

    let chaps = '';
    for(let titles in result){
        chaps = result[titles];
        db.raw('insert into chapters (novel, num, title, content) values(?, ?, ?, ?) on conflict do nothing', [novel[0], 1, titles, chaps])
        .then(console.log(titles));
    }
});

app.get('/novel/:link/:chap', (req, res) => {
    const filepath = 'python/scrapper.py';
    const spawn = require("child_process").spawn;
    const pyprocess = spawn('python',[filepath, req.params.link, req.params.chap, '-l']);

    pyprocess.stdout.on('data', (data) => {
        const text = data.toString('utf-8');
        const fin = JSON.parse(text)
        res.json(fin);
    })
});
 
app.listen(3000);