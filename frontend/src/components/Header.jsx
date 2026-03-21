import { NavLink, Link, useNavigate } from "react-router-dom";

export default function Header({ token, onLogout }) {
  const navigate = useNavigate();

  return (
    <header className="header">
      <div className="header-inner">
        <Link to="/" className="brand" aria-label="PhytoScan AI">
          <div className="brand-mark" aria-hidden="true">
            🌿
          </div>
          <div>
            <div className="brand-name">
              PhytoScan AI
              <span className="brand-sub">Vision + RAG pour vos cultures</span>
            </div>
          </div>
        </Link>

        <nav className="nav" aria-label="Navigation principale">
          <NavLink to="/" end className={({ isActive }) => (isActive ? "active" : "")}>
            Accueil
          </NavLink>
          <NavLink to="/about" className={({ isActive }) => (isActive ? "active" : "")}>
            À propos
          </NavLink>
          <NavLink
            to="/diagnostic"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Diagnostic
          </NavLink>
          <NavLink
            to="/assistant"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Assistant
          </NavLink>
          <NavLink
            to="/history"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Historique
          </NavLink>
        </nav>

        <div className="header-right">
          {token ? (
            <button
              type="button"
              className="btn btn-ghost"
              onClick={() => {
                onLogout();
                navigate("/");
              }}
            >
              Déconnexion
            </button>
          ) : (
            <button type="button" className="btn btn-primary" onClick={() => navigate("/login")}>
              Connexion
            </button>
          )}
        </div>
      </div>
    </header>
  );
}

