import { NavLink, useNavigate } from "react-router-dom";

export default function AdminHeader({ onLogout }) {
  const navigate = useNavigate();

  return (
    <header className="admin-header">
      <div className="admin-header-inner">
        <div className="admin-brand" aria-label="Admin PhytoScan AI">
          <div className="admin-brand-mark" aria-hidden="true">
            🛡️
          </div>
          <div>
            <div className="admin-brand-name">PhytoScan AI</div>
            <div className="admin-brand-sub">Console administrateur</div>
          </div>
        </div>

        <nav className="admin-top-nav" aria-label="Navigation admin">
          <NavLink
            to="/admin/dashboard"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Dashboard
          </NavLink>
          <NavLink
            to="/admin/users"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Utilisateurs
          </NavLink>
        </nav>

        <button
          type="button"
          className="btn btn-ghost"
          onClick={() => {
            onLogout();
            navigate("/login");
          }}
        >
          Déconnexion
        </button>
      </div>
    </header>
  );
}

