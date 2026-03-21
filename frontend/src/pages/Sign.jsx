import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { api } from "../api";

function sweetAlert({ title, text }) {
  return new Promise((resolve) => {
    const overlay = document.createElement("div");
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.style.cssText = `
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.45);
      display: grid;
      place-items: center;
      padding: 16px;
      z-index: 9999;
    `;

    const modal = document.createElement("div");
    modal.style.cssText = `
      width: min(460px, 100%);
      background: rgba(255, 255, 255, 0.96);
      border: 1px solid rgba(15, 23, 42, 0.12);
      border-radius: 16px;
      box-shadow: 0 18px 48px rgba(15, 23, 42, 0.18);
      padding: 18px;
      backdrop-filter: blur(10px);
    `;

    const head = document.createElement("div");
    head.style.cssText = "display:flex;align-items:flex-start;gap:12px;margin-bottom:10px;";

    const badge = document.createElement("div");
    badge.textContent = "✅";
    badge.style.cssText = `
      width: 44px; height: 44px;
      border-radius: 16px;
      display: grid; place-items: center;
      background: rgba(16,185,129,0.14);
      border: 1px solid rgba(16,185,129,0.24);
      flex: 0 0 auto;
    `;

    const titleEl = document.createElement("div");
    titleEl.textContent = title || "Succès";
    titleEl.style.cssText = "font-weight:800;letter-spacing:-0.01em;font-size:16px;color:#0f172a;";

    const textEl = document.createElement("div");
    textEl.textContent = text || "";
    textEl.style.cssText = "margin-top:6px;color:rgba(15,23,42,0.72);font-size:14px;line-height:1.6;";

    const body = document.createElement("div");
    body.appendChild(titleEl);
    body.appendChild(textEl);

    head.appendChild(badge);
    head.appendChild(body);

    const actions = document.createElement("div");
    actions.style.cssText = "display:flex;justify-content:flex-end;margin-top:14px;";

    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = "OK";
    btn.style.cssText = `
      border: 1px solid transparent;
      border-radius: 14px;
      padding: 10px 14px;
      cursor: pointer;
      font-weight: 700;
      background: linear-gradient(135deg, #10b981, #059669);
      color: #052e16;
      box-shadow: 0 12px 28px rgba(16,185,129,0.22);
    `;

    const cleanup = () => {
      overlay.removeEventListener("click", onOverlayClick);
      document.removeEventListener("keydown", onKeyDown);
      overlay.remove();
      resolve();
    };

    const onOverlayClick = (e) => {
      if (e.target === overlay) cleanup();
    };
    const onKeyDown = (e) => {
      if (e.key === "Escape") cleanup();
    };

    btn.addEventListener("click", cleanup);
    overlay.addEventListener("click", onOverlayClick);
    document.addEventListener("keydown", onKeyDown);

    actions.appendChild(btn);
    modal.appendChild(head);
    modal.appendChild(actions);
    overlay.appendChild(modal);
    document.body.appendChild(overlay);
  });
}

export default function Sign() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.register(username, email, password);
      await sweetAlert({
        title: "Inscription réussie",
        text: "Votre compte est créé. Vous pouvez maintenant vous connecter.",
      });
      navigate("/login");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="auth-shell">
      <div className="card auth-card">
        <div className="auth-head">
          <div className="page-kicker">
            <span className="pill">✨ Nouveau compte</span>
            <span className="pill">🌿 PhytoScan AI</span>
          </div>
          <h1 className="auth-title">Créer un compte</h1>
          <p className="p" style={{ fontSize: 14 }}>
            Accédez au diagnostic photo et à l’assistant agronomique. En quelques secondes, votre
            espace est prêt.
          </p>
        </div>

        {error && <div className="auth-error">⚠ {error}</div>}

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="auth-field">
            <label className="label" htmlFor="username">
              Nom d’agriculteur
            </label>
            <input
              id="username"
              className="input"
              type="text"
              placeholder="Ex : Ferme du Moulin"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="username"
            />
          </div>

          <div className="auth-field">
            <label className="label" htmlFor="email">
              Email
            </label>
            <input
              id="email"
              className="input"
              type="email"
              placeholder="vous@example.com"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
            />
          </div>

          <div className="auth-field">
            <label className="label" htmlFor="password">
              Mot de passe
            </label>
            <input
              id="password"
              className="input"
              type="password"
              placeholder="••••••••"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="new-password"
            />
          </div>

          <div className="auth-actions">
            <button className="btn btn-primary" type="submit" style={{ width: "100%" }}>
              S’inscrire →
            </button>
            <p className="auth-help" style={{ margin: 0 }}>
              Déjà un compte ? <Link to="/login">Se connecter</Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
}