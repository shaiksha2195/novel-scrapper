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


app.get('/add/:link', (req, res) => {
    
    const filepath = 'python/scrapper.py';
    const spawn = require("child_process").spawn;
    const pyprocess = spawn('python',[filepath, req.params.link.toString()]);
    
    pyprocess.stdout.on('data', (data) => {
    const text = data.toString('utf-8');
    console.log(text);
    });
    
    res.send("Adding the Novel!");
});
  
app.get('/:link/:chap', (req, res) => {
  let jsonfile = require('../novels/' + req.params.link.toString() +'.json');
  let num = parseInt(req.params.chap) - 1;
  try{
    let x = '<h2 class = "title">' + Object.keys(jsonfile)[num] + '</h2>'
            + Object.values(jsonfile)[num];
    let sel;
    let i = 1;
    let j = num +1;
    Object.keys(jsonfile).forEach(element => {
      if(j  === i)
      {
        sel += "<option value = '"+ i +"' selected>"+ element+1 + "</option>";
      }
      else{
        sel += "<option value = '"+ i +"'>"+ element+1 + "</option>";
      }
      i++;
    });

    let options = "<button><a href='" + num++ + "'>Prev</a></button><select  onchange='location = this.value;'>" + sel + "</select><button><a href='"+ ++num + "'>Next</a></button><button><a href='http://localhost:3000'>HOME</a></button>";
    let result = options + x + options;

    if( Object.keys(jsonfile)[num] === undefined)
    {
      res.send(options + "<br>no such novel or chapter!")
    }
    else{
      res.send("<div style='padding-bottom:100px;'>" + result + "</div>");
    }
  }
  catch{
    res.send("no such novel or chapter!")
  }
});

app.get('/', (req, res) => {
  const folder = '../novels';
  let list = '';
  let i = 0;
  fs.readdir(folder, (err, files) => {
    files.forEach(el => {
      if (i == 0)
        i++;
      else
        list += '<li><a href="/' + el.split('.')[0] + '/1" style="text-decoration:none;color:black">' + el.split('.')[0] + '</a></li>';
    });
    res.send('<h2>Novels</h2><ul style="list-style:none">' + list + '</ul>');
  });
});


app.listen(3000);