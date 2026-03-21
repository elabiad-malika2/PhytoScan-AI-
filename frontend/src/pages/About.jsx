import { Link } from "react-router-dom";

export default function About() {
  return (
    <div className="container">
      <div className="page-head">
        <div className="page-kicker">
          <span className="pill">🌾 Notre mission</span>
          <span className="pill">🔎 Vision + RAG</span>
          <span className="pill">🧠 Aide à la décision</span>
        </div>
        <h1 className="h1">À propos de PhytoScan AI</h1>
        <p className="p" style={{ fontSize: 15 }}>
          PhytoScan AI est né d’un constat simple : sur le terrain, chaque minute compte. Notre but
          est d’aider les agriculteurs à identifier plus vite les maladies, à comprendre les causes
          probables, et à agir avec méthode.
        </p>
      </div>

      <div className="grid-3" style={{ marginTop: 14 }}>
        <div className="card feature">
          <div className="feature-icon" aria-hidden="true">
            🌿
          </div>
          <h3>Protéger les récoltes</h3>
          <p>
            Réduire les pertes et améliorer la réactivité, en apportant un diagnostic clair et
            actionnable.
          </p>
        </div>
        <div className="card feature">
          <div className="feature-icon" aria-hidden="true">
            🤝
          </div>
          <h3>Épauler la décision</h3>
          <p>
            L’outil assiste, il ne remplace pas l’expertise. Il aide à cadrer les prochaines
            actions.
          </p>
        </div>
        <div className="card feature">
          <div className="feature-icon" aria-hidden="true">
            🧾
          </div>
          <h3>Rendre les infos partageables</h3>
          <p>
            Rapports structurés et export PDF pour échanger facilement avec une équipe ou un
            conseiller.
          </p>
        </div>
      </div>

      <div className="card" style={{ padding: 18, marginTop: 14 }}>
        <h2 className="h2">Pourquoi Vision + RAG ?</h2>
        <p className="p" style={{ marginTop: 8 }}>
          La Vision IA reconnaît des motifs visuels (taches, nécroses, décolorations). Le RAG
          (Retrieval-Augmented Generation) ajoute une couche de fiabilité en s’appuyant sur des
          ressources pertinentes (guides, recommandations, documents techniques) pour contextualiser
          la réponse.
        </p>
        <div style={{ height: 12 }} />
        <div className="grid-3">
          <div className="card feature" style={{ background: "rgba(255,255,255,0.75)" }}>
            <div className="feature-icon" aria-hidden="true">
              🧠
            </div>
            <h3>Moins d’hallucinations</h3>
            <p>Le modèle s’ancre sur des extraits récupérés, au lieu d’inventer.</p>
          </div>
          <div className="card feature" style={{ background: "rgba(255,255,255,0.75)" }}>
            <div className="feature-icon" aria-hidden="true">
              🎯
            </div>
            <h3>Plus de précision</h3>
            <p>Une meilleure pertinence sur les traitements et les mesures préventives.</p>
          </div>
          <div className="card feature" style={{ background: "rgba(255,255,255,0.75)" }}>
            <div className="feature-icon" aria-hidden="true">
              🔍
            </div>
            <h3>Traçabilité</h3>
            <p>Des sources peuvent être affichées pour faciliter la vérification.</p>
          </div>
        </div>
      </div>

      <div style={{ marginTop: 16, display: "flex", gap: 12, flexWrap: "wrap" }}>
        <Link className="btn btn-primary" to="/diagnostic">
          Lancer un diagnostic →
        </Link>
        <Link className="btn btn-ghost" to="/assistant">
          Ouvrir l’assistant
        </Link>
      </div>
    </div>
  );
}

