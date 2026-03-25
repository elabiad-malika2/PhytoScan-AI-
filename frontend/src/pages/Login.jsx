import { useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";

export default function Login({ setToken }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const extractRoleFromJwt = (jwt) => {
    try {
      const parts = (jwt || "").split(".");
      if (parts.length < 2) return null;
      const base64Url = parts[1];
      const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split("")
          .map((c) => `%${("00" + c.charCodeAt(0).toString(16)).slice(-2)}`)
          .join("")
      );
      const payload = JSON.parse(jsonPayload);
      return payload?.role || null;
    } catch {
      return null;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await api.login(email, password);
      localStorage.setItem("token", data.access_token);
      const role = extractRoleFromJwt(data.access_token);
      if (role) localStorage.setItem("role", role);
      setToken(data.access_token);
    } catch {
      setError("Email ou mot de passe incorrect");
    }
  };

  return (
    <div className="auth-shell">
      <div className="card auth-card">
        <div className="auth-head">
          <div className="page-kicker">
            <span className="pill">🔒 Espace sécurisé</span>
            <span className="pill">🌿 PhytoScan AI</span>
          </div>
          <h1 className="auth-title">Connexion</h1>
          <p className="p" style={{ fontSize: 14 }}>
            Connectez-vous pour lancer un diagnostic et accéder à l’assistant agronomique.
          </p>
        </div>

        {error && <div className="auth-error">⚠ {error}</div>}

        <form className="auth-form" onSubmit={handleSubmit}>
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
              autoComplete="current-password"
            />
          </div>

          <div className="auth-actions">
            <button className="btn btn-primary" type="submit" style={{ width: "100%" }}>
              Se connecter →
            </button>
            <p className="auth-help">
              Astuce : vous pouvez d’abord explorer la page d’accueil, puis vous connecter au moment
              du diagnostic.
            </p>
            <div style={{ display: "grid", gap: 10 }}>
              <div
                style={{
                  height: 1,
                  background: "rgba(15, 23, 42, 0.08)",
                  marginTop: 2,
                }}
              />
              <p className="auth-help" style={{ margin: 0 }}>
                Pas encore de compte ? <Link to="/sign">Créer un compte</Link>
              </p>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}