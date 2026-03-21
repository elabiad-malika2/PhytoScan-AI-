import { useState, useEffect, useRef } from "react";
import { api } from "../api";
import Markdown from "../components/Markdown";

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Charger l'historique des recherches au démarrage
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        setLoading(true);
        const historyData = await api.getChatHistory();
        // Backend: plus récent -> plus ancien, on affiche du plus récent au plus ancien
        setMessages(Array.isArray(historyData) ? historyData : []);
      } catch (error) {
        console.error("Erreur lors du chargement de l'historique", error);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  // Scroll vers le résultat après une nouvelle recherche
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const question = input;
    setInput("");
    setLoading(true);

    try {
      const response = await api.askChatbot(question);
      const entry = {
        id: `local-${Date.now()}`,
        query: question,
        response: response.rapport_ia,
        created_at: new Date().toISOString(),
        ressource_officielle: response.ressource_officielle,
      };
      setMessages((prev) => [entry, ...(prev || [])]);
    } catch {
      const entry = {
        id: `local-${Date.now()}`,
        query: question,
        response: " Désolé, je n'ai pas pu trouver d'informations à ce sujet. Veuillez réessayer.",
        created_at: new Date().toISOString(),
        ressource_officielle: null,
      };
      setMessages((prev) => [entry, ...(prev || [])]);
    } finally {
      setLoading(false);
    }
  };

  const latest = messages?.[0];
  const latestDate = latest?.created_at ? new Date(latest.created_at) : null;

  return (
    <div className="container">
      <div className="page-head">
        <div className="page-kicker">
          <span className="pill">🔎 Moteur agronomique</span>
          <span className="pill">📚 Sources</span>
          <span className="pill">🧠 RAG</span>
        </div>
        <h2 className="h2">Moteur de recherche agronomique</h2>
        <p className="p" style={{ fontSize: 14 }}>
          Recherchez une maladie ou décrivez des symptômes. Chaque requête est indépendante (pas de
          mémoire conversationnelle), pour des résultats plus fiables et mieux traçables.
        </p>
      </div>

      <div className="card search-panel">
        <form className="search-form" onSubmit={handleSend}>
          <div style={{ display: "grid", gap: 6 }}>
            <label className="label" htmlFor="agro-query">
              Votre recherche
            </label>
            <input
              id="agro-query"
              className="input search-input"
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Entrez le nom d’une maladie… ex: Mildiou de la tomate, taches brunes sur feuille…"
              disabled={loading}
              aria-label="Entrez votre recherche agronomique"
            />
          </div>

          <button className="btn btn-primary search-action" type="submit" disabled={loading || !input.trim()}>
            {loading ? "Recherche…" : "Demander à l’expert →"}
          </button>
        </form>

        {loading && (
          <div className="search-skeleton" aria-label="Chargement">
            <div className="skeleton-line" style={{ width: "55%" }} />
            <div className="skeleton-line" />
            <div className="skeleton-line" />
            <div className="skeleton-line" style={{ width: "80%" }} />
          </div>
        )}
      </div>

      {latest && !loading && (
        <div className="card search-result" style={{ marginTop: 12 }}>
          <div className="rx-head">
            <div className="rx-badge" aria-hidden="true">
              🧾
            </div>
            <div style={{ flex: 1 }}>
              <p className="rx-label">Question posée</p>
              <p className="rx-title" style={{ fontSize: 16 }}>
                {latest.query}
              </p>
              {latestDate && (
                <div className="rx-meta" style={{ marginTop: 6 }}>
                  {latestDate.toLocaleDateString("fr-FR")} ·{" "}
                  {latestDate.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" })}
                </div>
              )}
            </div>
          </div>

          <div className="rx-body">
            <div>
              <p className="label" style={{ marginBottom: 8 }}>
                Rapport d’expertise
              </p>
              <Markdown className="rx-report" text={latest.response} />
            </div>

            <div className="rx-meta" style={{ display: "flex", gap: 10, flexWrap: "wrap", alignItems: "center" }}>
              <span className="pill">📌 Résultat indépendant</span>
              <span className="pill">
                📚 Source : {latest.ressource_officielle || "Non précisée"}
              </span>
            </div>

            <div ref={messagesEndRef} />
          </div>
        </div>
      )}

      <div className="section" style={{ marginTop: 16 }}>
        <div className="section-head" style={{ marginBottom: 10 }}>
          <h2 className="h2" style={{ fontSize: 18 }}>
            Historique des recherches
          </h2>
          <p className="p" style={{ fontSize: 13 }}>
            Chaque carte correspond à une recherche distincte. Ouvrez pour voir le rapport complet.
          </p>
        </div>

        {messages.length === 0 && !loading ? (
          <div className="card" style={{ padding: 16 }}>
            <p className="p">Aucune recherche enregistrée pour le moment.</p>
          </div>
        ) : (
          <div className="history-list">
            {messages.map((item) => {
              const d = item?.created_at ? new Date(item.created_at) : null;
              return (
                <details key={item.id} className="history-item">
                  <summary className="history-summary">
                    <div style={{ display: "grid", gap: 4 }}>
                      <span className="history-label">Question posée</span>
                      <span className="history-question">{item.query}</span>
                    </div>
                    <div className="history-meta">
                      {d
                        ? `${d.toLocaleDateString("fr-FR")} · ${d.toLocaleTimeString("fr-FR", {
                          hour: "2-digit",
                          minute: "2-digit",
                        })}`
                        : "—"}
                    </div>
                  </summary>

                  <div className="history-body">
                    <div>
                      <span className="history-label">Réponse de l’IA</span>
                      <div style={{ height: 8 }} />
                      <Markdown className="rx-report" text={item.response} />
                    </div>
                    <div className="rx-meta" style={{ marginTop: 10 }}>
                      📚 Source : {item.ressource_officielle || "Non précisée"}
                    </div>
                  </div>
                </details>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}