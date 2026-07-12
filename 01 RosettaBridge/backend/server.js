const express = require('express');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();
const { exec } = require('child_process');

const app = express();
const PORT = process.env.PORT || 4000;

// Conexión a la base de datos usando la ruta absoluta correcta
const dbPath = '/home/prolog/Desktop/01 DevVault_2026/01 RosettaBridge/database/clinic.db';
const db = new sqlite3.Database(dbPath, (err) => {
    if (err) {
        console.error("Error al conectar con la base de datos:", err.message);
    } else {
        console.log("Conectado a la base de datos SQLite.");
    }
});

app.use(express.json());

// Como public está dentro de backend, usamos __dirname directamente
const publicPath = path.join(__dirname, 'public');
app.use(express.static(publicPath));

// Ruta principal para servir la interfaz
app.get('/', (req, res) => {
    res.sendFile(path.join(publicPath, 'index.html'));
});

// Endpoint para obtener todos los registros de pacientes
app.get('/api/records', (req, res) => {
    db.all("SELECT rowid as record_number, id, nombre, dire, telefono, eddad, colesterol, glicemia FROM pacientes", [], (err, rows) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(rows);
    });
});

// Endpoint para guardar un nuevo registro vía POST
app.post('/api/records', (req, res) => {
    const { id, nombre, dire, telefono, eddad, colesterol, glicemia } = req.body;
    const query = `INSERT INTO pacientes (id, nombre, dire, telefono, eddad, colesterol, glicemia) VALUES (?, ?, ?, ?, ?, ?, ?)`;
    
    db.run(query, [id, nombre, dire, telefono, eddad, colesterol, glicemia], function(err) {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ success: true, id: this.lastID });
    });
});

// Endpoint para obtener estadísticas usando rutas absolutas exactas
app.get('/api/stats', (req, res) => {
    const pythonCmd = '"/home/prolog/Desktop/01 DevVault_2026/01 RosettaBridge/venv/bin/python3"';
    const scriptPath = '"/home/prolog/Desktop/01 DevVault_2026/01 RosettaBridge/engines/Python/stats.py"';
    
    exec(`${pythonCmd} ${scriptPath}`, (error, stdout, stderr) => {
        if (error) {
            console.error("Error ejecutando Python:", stderr);
            return res.status(500).json({ error: stderr });
        }
        try {
            const output = stdout.trim();
            const jsonStart = output.indexOf('{');
            const cleanJson = jsonStart !== -1 ? output.substring(jsonStart) : output;
            res.json(JSON.parse(cleanJson));
        } catch (e) {
            console.error("Error parseando JSON de Python:", e.message, "Stdout fue:", stdout);
            res.status(500).json({ error: "No se pudo parsear el JSON de Python" });
        }
    });
});

app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});