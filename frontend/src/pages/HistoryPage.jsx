import { useState, useEffect } from "react";
import { api } from "../api";

export default function HistoryPage() {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const data = await api.getScanHistory();
      setScans(data);
    } catch (error) {
      console.error(error);
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
      a.download = `Diagnostic_${(diseaseLabel || `scan_${scanId}`)
        .toString()
        .replaceAll(" ", "_")}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(error);
      alert("Impossible de télécharger le PDF. Veuillez vous reconnecter et réessayer.");
    }
  };

  return (
    <div className="container">
      <div className="page-head">
        <div className="page-kicker">
          <span className="pill">📂 Historique</span>
          <span className="pill">🧾 PDF</span>
          <span className="pill">🔎 Traçabilité</span>
        </div>
        <h2 className="h2">Mon historique de diagnostics</h2>
        <p className="p" style={{ fontSize: 14 }}>
          Retrouvez toutes vos analyses et téléchargez vos rapports PDF. Pratique pour suivre
          l’évolution et partager avec un conseiller.
        </p>
      </div>

      {loading ? (
        <div className="card" style={{ padding: 16 }}>
          <p className="p">Chargement de l’historique…</p>
        </div>
      ) : scans.length === 0 ? (
        <div className="card" style={{ padding: 16 }}>
          <p className="p" style={{ marginBottom: 10 }}>
            Vous n’avez pas encore scanné de plante.
          </p>
          <p className="p" style={{ fontSize: 13 }}>
            Lancez votre premier diagnostic depuis l’onglet Diagnostic.
          </p>
        </div>
      ) : (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))",
            gap: 12,
          }}
        >
          {scans.map((scan) => {
            const created = new Date(scan.created_at);
            const disease = (scan.disease_detected || "").replace(/_/g, " ");
            const rawImage = scan.image_url || scan.image_path || "";
            const filename = rawImage
              ? rawImage.split("/").pop()?.split("\\").pop()
              : "";
            const normalizedImagePath =
              rawImage.includes("/uploads/")
                ? rawImage.slice(rawImage.indexOf("/uploads/"))
                : rawImage.includes("/app/data/uploads/") || rawImage.includes("\\app\\data\\uploads\\")
                  ? `/uploads/${filename}`
                  : rawImage.startsWith("/")
                    ? rawImage
                    : filename
                      ? `/uploads/${filename}`
                      : "";
            const imageSrc =
              normalizedImagePath && (normalizedImagePath.startsWith("http://") || normalizedImagePath.startsWith("https://"))
                ? normalizedImagePath
                : `http://localhost:8000${normalizedImagePath}`;
            return (
              <div key={scan.id} className="card" style={{ overflow: "hidden" }}>
                <div style={{ padding: 12, borderBottom: "1px solid rgba(15, 23, 42, 0.08)" }}>
                  <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
                    <span className="pill">🩺 Diagnostic</span>
                    <span className="pill">
                      {created.toLocaleDateString("fr-FR")} ·{" "}
                      {created.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" })}
                    </span>
                  </div>
                  <div style={{ height: 10 }} />
                  <p
                    className="h2"
                    style={{
                      fontSize: 16,
                      margin: 0,
                      textTransform: "capitalize",
                    }}
                  >
                    {disease || "Maladie non spécifiée"}
                  </p>
                </div>

                <div style={{ padding: 12, display: "grid", gap: 10 }}>
                  <div style={{ borderRadius: 16, overflow: "hidden", border: "1px solid rgba(15, 23, 42, 0.08)" }}>
                    <img
                      src={imageSrc}
                      alt="Plante"
                      style={{ width: "100%", height: 180, objectFit: "cover", display: "block" }}
                      loading="lazy"
                    />
                  </div>

                  <div className="rx-meta">
                    ID scan : <span style={{ fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace" }}>{scan.id}</span>
                  </div>

                  <button
                    type="button"
                    className="btn btn-pdf"
                    onClick={() => handleDownloadPdf(scan.id, disease)}
                    style={{ width: "100%" }}
                  >
                    📄 Télécharger le Rapport PDF
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}