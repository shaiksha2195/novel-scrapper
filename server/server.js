const express = require('express');
const app = express();

app.get('/novel/:link', (req, res) => {
    const filepath = 'python/scrapper.py';
    const spawn = require("child_process").spawn;
    const pyprocess = spawn('python',[filepath, req.params.link, '-l']);

    pyprocess.stdout.on('data', (data) => {
        const text = data.toString('utf-8');
        const fin = JSON.parse(text)
        res.json(fin);
    })
});
 
app.listen(3000);