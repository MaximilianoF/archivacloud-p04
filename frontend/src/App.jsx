import { useState, useEffect } from "react";
import axios from "axios";

const API = "http://127.0.0.1:8000";

function App() {
  const [files, setFiles] = useState([]);
  const [file, setFile] = useState(null);
  const [mensaje, setMensaje] = useState("");
  const [cargando, setCargando] = useState(false);

  useEffect(() => {
    listarArchivos();
  }, []);

  const listarArchivos = async () => {
    try {
      const res = await axios.get(`${API}/api/files`);
      setFiles(res.data);
    } catch {
      setMensaje("Error al listar archivos");
    }
  };

  const subirArchivo = async () => {
    if (!file) return;
    setCargando(true);
    setMensaje("");
    try {
      const res = await axios.post(`${API}/api/upload/presigned-url`, {
        fileName: file.name,
        fileType: file.type,
        fileSize: file.size,
      });
      await axios.put(res.data.presignedUrl, file, {
        headers: { "Content-Type": file.type },
      });
      setMensaje("Archivo subido correctamente");
      listarArchivos();
    } catch (err) {
      setMensaje(err.response?.data?.detail || "Error al subir archivo");
    }
    setCargando(false);
  };

  const eliminarArchivo = async (key) => {
    if (!window.confirm("¿Eliminar este archivo?")) return;
    try {
      await axios.delete(`${API}/api/files/${encodeURIComponent(key)}`);
      setMensaje("Archivo eliminado");
      listarArchivos();
    } catch {
      setMensaje("Error al eliminar");
    }
  };

  const exportarCSV = () => {
    const encabezado = "Nombre,Tamaño (bytes),Fecha\n";
    const filas = files.map(f => `${f.nombre},${f.tamaño},${f.fecha}`).join("\n");
    const blob = new Blob([encabezado + filas], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "archivos.csv";
    a.click();
  };

  return (
    <div style={{ maxWidth: 700, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>ArchivaCloud P-04</h1>
      <p>Archivos permitidos: CSV, XLSX — Máximo 25 MB</p>

      <div style={{ marginBottom: 16 }}>
        <input type="file" accept=".csv,.xlsx" onChange={e => setFile(e.target.files[0])} />
        <button onClick={subirArchivo} disabled={cargando} style={{ marginLeft: 8 }}>
          {cargando ? "Subiendo..." : "Subir"}
        </button>
      </div>

      {mensaje && <p style={{ color: "green" }}>{mensaje}</p>}

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h2>Archivos en el bucket</h2>
        <button onClick={exportarCSV}>Exportar CSV</button>
      </div>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#f0f0f0" }}>
            <th style={{ padding: 8, textAlign: "left" }}>Nombre</th>
            <th style={{ padding: 8 }}>Tamaño</th>
            <th style={{ padding: 8 }}>Fecha</th>
            <th style={{ padding: 8 }}>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {files.map((f, i) => (
            <tr key={i} style={{ borderBottom: "1px solid #ddd" }}>
              <td style={{ padding: 8 }}>{f.nombre}</td>
              <td style={{ padding: 8, textAlign: "center" }}>{f.tamaño} bytes</td>
              <td style={{ padding: 8, textAlign: "center" }}>{f.fecha}</td>
              <td style={{ padding: 8, textAlign: "center" }}>
                <a href={f.url} target="_blank" rel="noreferrer">Descargar</a>
                {" | "}
                <button onClick={() => eliminarArchivo(f.key)}>Eliminar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;