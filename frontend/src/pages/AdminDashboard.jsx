import { useEffect, useState } from "react";
import { api } from "../api";

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    api.getAdminDashboard().then(setStats).catch(console.error);
  }, []);

  return (
    <div className="container">
      <div className="page-head">
        <div className="page-kicker">
          <span className="pill">🛠 Admin</span>
          <span className="pill">📊 Surveille l’usage</span>
        </div>
        <h2 className="h2">Tableau de bord administrateur</h2>
        <p className="p" style={{ fontSize: 14 }}>
          Vue globale sur l’activité de la plateforme : nombre d’agriculteurs, volume d’analyses et
          de recherches textuelles.
        </p>
      </div>

      {!stats ? (
        <div className="card" style={{ padding: 16, marginTop: 12 }}>
          <p className="p">Chargement des statistiques…</p>
        </div>
      ) : (
        <>
          <div className="admin-grid">
            <div className="card admin-stat">
              <div className="admin-stat-header">
                <span className="pill">👨‍🌾 Utilisateurs</span>
              </div>
              <p className="admin-stat-label">Agriculteurs inscrits</p>
              <p className="admin-stat-value">{stats.total_agriculteurs}</p>
            </div>

            <div className="card admin-stat">
              <div className="admin-stat-header">
                <span className="pill">📷 Vision</span>
              </div>
              <p className="admin-stat-label">Plantes scannées</p>
              <p className="admin-stat-value">{stats.total_scans_realises}</p>
            </div>

            <div className="card admin-stat">
              <div className="admin-stat-header">
                <span className="pill">💬 Texte</span>
              </div>
              <p className="admin-stat-label">Questions posées</p>
              <p className="admin-stat-value">{stats.total_questions_posees}</p>
            </div>
          </div>

          <div className="card" style={{ padding: 16, marginTop: 14 }}>
            <p className="label" style={{ marginBottom: 8 }}>
              Synthèse rapide
            </p>
            <p className="p" style={{ fontSize: 13.5 }}>
              Vous pouvez utiliser ces indicateurs pour suivre l’adoption de PhytoScan AI :{" "}
              <strong>nombre d’agriculteurs actifs</strong>,{" "}
              <strong>fréquence d’analyse des cultures</strong> et{" "}
              <strong>usage du moteur de recherche agronomique</strong>.
            </p>
          </div>
        </>
      )}
    </div>
  );
}