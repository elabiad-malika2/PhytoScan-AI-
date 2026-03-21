import { useState } from "react";
import { api } from "../api";
import Markdown from "../components/Markdown";

export default function ScanPage() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    setFile(selected);
    if (selected) {
      setPreview(URL.createObjectURL(selected));
    }
  };

  const handleScan = async () => {
    if (!file) return alert("Veuillez sélectionner une image");
    setLoading(true);
    try {
      const data = await api.analyzeScan(file);
      setResult(data);
    } catch {
      alert("Erreur lors de l'analyse");
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPdf = async (scanId, diseaseLabel) => {
    try {
      const blob = await api.downloadReport(scanId);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `Diagnostic_${(diseaseLabel || "rapport").toString().replaceAll(" ", "_")}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch {
      alert("Impossible de télécharger le PDF. Veuillez vous reconnecter et réessayer.");
    }
  };

  return (
    <div className="container">
      <div className="page-head">
        <div className="page-kicker">
          <span className="pill">📷 Diagnostic photo</span>
          <span className="pill">🔬 Vision IA</span>
          <span className="pill">🧾 Rapport PDF</span>
        </div>
        <h2 className="h2">Scanner une plante</h2>
        <p className="p" style={{ fontSize: 14 }}>
          Glissez-déposez une image ou cliquez pour l’importer. L’analyse IA détecte la maladie et
          génère un rapport expert.
        </p>
      </div>

      <div className="dropzone" data-active={file ? "true" : "false"}>
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <div className="dropzone-inner">
          <div className="dropzone-icon" aria-hidden="true">
            📸
          </div>
          <p className="dropzone-title">
            {file ? "Image prête pour l’analyse" : "Glissez-déposez votre photo ici"}
          </p>
          <p className="dropzone-hint">ou cliquez pour sélectionner (JPG/PNG/WEBP — max 10 Mo)</p>
          {file && <span className="file-pill">✓ {file.name}</span>}
        </div>
      </div>

      {preview && (
        <div className="preview">
          <img src={preview} alt="Aperçu" />
        </div>
      )}

      <div style={{ marginTop: 12 }}>
        <button className="btn btn-primary" onClick={handleScan} disabled={loading || !file} style={{ width: "100%" }}>
          {loading ? "Analyse en cours..." : "Lancer l’analyse IA →"}
        </button>
        <p className="p" style={{ marginTop: 10, fontSize: 12 }}>
          Conseil : privilégiez une photo nette et proche de la zone atteinte (feuille, tige, fruit).
        </p>
      </div>

      {result && (
        <>
          <hr className="divider" />
          <div className="card rx-card">
            <div className="rx-head">
              <div className="rx-badge" aria-hidden="true">
                🩺
              </div>
              <div>
                <p className="rx-label">Diagnostic détecté</p>
                <p className="rx-title">{result.maladie_detectee}</p>
              </div>
            </div>

            <div className="rx-body">
              <div className="preview" style={{ marginTop: 0 }}>
                <img src={`http://localhost:8000${result.image_url}`} alt="Plante analysée" />
              </div>

              <div>
                <p className="label" style={{ marginBottom: 8 }}>
                  Rapport expert IA
                </p>
                <Markdown className="rx-report" text={result.rapport_expert} />
              </div>

              <div className="rx-meta">📚 Source : {result.source}</div>

              <button
                type="button"
                className="btn btn-pdf"
                onClick={() => handleDownloadPdf(result.scan_id, result.maladie_detectee)}
                style={{ width: "100%" }}
              >
                📄 Télécharger le PDF
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}