const express = require('express');
const app = express();

app.get('/', (req, res) => {
    const filepath = 'python';
    const spawn = require("child_process").spawn;
    const pyprocess = spawn('python3',[filepath, '-l']);

    Uint8ClampedArray.log('readingin')
    pyprocess.stdout.on('data', (data) => {
        const text = data.toString('utf-8');
        util.log(text);
        res.json({'data':text});
    })

});

app.listen(3000);