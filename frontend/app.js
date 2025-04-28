const express = require('express');
const app = express();
const path = require('path');
const axios = require('axios');

app.use(express.static(path.join(__dirname, 'public')));

app.get('/increment', async (req, res) => {
    await axios.get('http://backend:8000/increment');
    res.redirect('/');
});

app.get('/get', async (req, res) => {
    const response = await axios.get('http://backend:8000/get');
    res.send(`
        <h1>Current Counter: ${response.data.count}</h1>
        <a href="/">Go Back</a>
    `);
});

app.get('/', (req, res) => {
    res.send(`
        <h1>Counter App</h1>
        <button onclick="location.href='/increment'">Increment Counter</button>
        <button onclick="location.href='/get'">Get Counter</button>
    `);
});

app.listen(3000, () => console.log('Frontend running on port 3000'));
