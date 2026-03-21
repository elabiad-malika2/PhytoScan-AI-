import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container" style={{ paddingTop: 22, paddingBottom: 18 }}>
        <div className="footer-grid">
          <div>
            <p className="footer-title">PhytoScan AI</p>
            <p className="p" style={{ fontSize: 13 }}>
              Diagnostic des maladies des plantes par Vision IA et recommandations fiables via RAG,
              pensées pour le terrain.
            </p>
            <div style={{ marginTop: 12, display: "flex", gap: 10, flexWrap: "wrap" }}>
              <span className="pill">🌱 AgriTech</span>
              <span className="pill">🔬 Diagnostic</span>
              <span className="pill">📚 Sources officielles</span>
            </div>
          </div>

          <div>
            <p className="footer-title">Liens rapides</p>
            <div className="footer-links">
              <Link to="/">Accueil</Link>
              <Link to="/about">À propos</Link>
              <Link to="/diagnostic">Diagnostic</Link>
              <Link to="/assistant">Assistant</Link>
            </div>
          </div>

          <div>
            <p className="footer-title">Réseaux & légal</p>
            <div className="footer-links">
              <a href="#" onClick={(e) => e.preventDefault()}>
                Mentions légales
              </a>
              <a href="#" onClick={(e) => e.preventDefault()}>
                Politique de confidentialité
              </a>
              <a href="#" onClick={(e) => e.preventDefault()}>
                LinkedIn
              </a>
              <a href="#" onClick={(e) => e.preventDefault()}>
                X (Twitter)
              </a>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <span>© 2026 PhytoScan AI. Tous droits réservés.</span>
          <span>Conçu pour mobile, optimisé pour le champ.</span>
        </div>
      </div>
    </footer>
  );
}

