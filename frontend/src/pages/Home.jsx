import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="container">
      <section className="hero">
        <div className="hero-grid">
          <div className="card hero-card">
            <div className="page-kicker">
              <span className="pill">⚡ Diagnostic en quelques secondes</span>
              <span className="pill">📷 Photo → Analyse → Traitement</span>
            </div>

            <h1 className="h1" style={{ marginTop: 12 }}>
              L’Intelligence Artificielle au service de vos cultures
            </h1>
            <p className="p" style={{ marginTop: 10, fontSize: 15 }}>
              Prenez une photo, obtenez un diagnostic et des recommandations claires, appuyées par
              des sources officielles. Pensé pour les agriculteurs, sur mobile, dans les champs.
            </p>

            <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginTop: 16 }}>
              <Link className="btn btn-primary" to="/diagnostic">
                Démarrer un diagnostic gratuit →
              </Link>
              <Link className="btn btn-ghost" to="/about">
                Découvrir la méthode
              </Link>
            </div>

            <div className="stat-grid">
              <div className="stat">
                <strong>Vision IA</strong>
                <span>Détection rapide des maladies</span>
              </div>
              <div className="stat">
                <strong>RAG</strong>
                <span>Réponses ancrées dans des sources</span>
              </div>
              <div className="stat">
                <strong>Mobile-first</strong>
                <span>Interface lisible en extérieur</span>
              </div>
              <div className="stat">
                <strong>PDF</strong>
                <span>Rapports prêts à partager</span>
              </div>
            </div>
          </div>

          <div className="hero-art">
            <div className="pill">🌿 AgriTech moderne</div>
            <div style={{ height: 12 }} />
            <p className="h2" style={{ marginBottom: 10 }}>
              Un assistant agronomique, dans votre poche.
            </p>
            <p className="p" style={{ fontSize: 13 }}>
              Construit pour guider la décision, pas pour noyer d’informations. Des étapes simples,
              une lecture claire, des recommandations actionnables.
            </p>
            <div style={{ height: 14 }} />
            <div className="card" style={{ padding: 14, background: "rgba(255,255,255,0.72)" }}>
              <div style={{ display: "grid", gap: 10 }}>
                <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
                  <span className="pill">1</span>
                  <span style={{ fontWeight: 700 }}>Photo de la plante</span>
                </div>
                <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
                  <span className="pill">2</span>
                  <span style={{ fontWeight: 700 }}>Analyse IA</span>
                </div>
                <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
                  <span className="pill">3</span>
                  <span style={{ fontWeight: 700 }}>Traitement & prévention</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <h2 className="h2">Comment ça marche</h2>
          <p className="p">Un parcours simple, conçu pour les conditions réelles de terrain.</p>
        </div>

        <div className="grid-3">
          <div className="card feature">
            <div className="feature-icon" aria-hidden="true">
              📷
            </div>
            <h3>Prenez une photo</h3>
            <p>Importez une image nette de la feuille, de la tige ou du fruit concerné.</p>
          </div>
          <div className="card feature">
            <div className="feature-icon" aria-hidden="true">
              🤖
            </div>
            <h3>L’IA analyse</h3>
            <p>La Vision détecte la maladie, puis le RAG consolide la réponse avec du contexte.</p>
          </div>
          <div className="card feature">
            <div className="feature-icon" aria-hidden="true">
              🧾
            </div>
            <h3>Obtenez le traitement</h3>
            <p>Recevez un rapport clair, des actions prioritaires, et un PDF téléchargeable.</p>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="section-head">
          <h2 className="h2">Pourquoi nous choisir ?</h2>
          <p className="p">
            Un produit “SaaS-ready” : fiable, lisible, et rapide — avec des détails qui comptent.
          </p>
        </div>

        <div className="grid-3">
          <div className="card feature">
            <div className="feature-icon" aria-hidden="true">
              ✅
            </div>
            <h3>Clarté avant tout</h3>
            <p>Des résultats structurés, faciles à expliquer à une équipe ou à un conseiller.</p>
          </div>
          <div className="card feature">
            <div className="feature-icon" aria-hidden="true">
              📚
            </div>
            <h3>Sources traçables</h3>
            <p>Le chatbot cite des ressources officielles lorsque disponibles.</p>
          </div>
          <div className="card feature">
            <div className="feature-icon" aria-hidden="true">
              📱
            </div>
            <h3>Mobile-first</h3>
            <p>Confort de lecture et zones tactiles, même en plein soleil.</p>
          </div>
        </div>
      </section>
    </div>
  );
}

