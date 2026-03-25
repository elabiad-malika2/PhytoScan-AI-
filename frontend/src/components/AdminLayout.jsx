import { NavLink } from "react-router-dom";
import AdminHeader from "./AdminHeader";
import AdminFooter from "./AdminFooter";

export default function AdminLayout({ children, onLogout }) {
  return (
    <div className="admin-shell">
      <AdminHeader onLogout={onLogout} />

      <div className="admin-body">
        <aside className="admin-sidebar" aria-label="Navigation latérale admin">
          <div className="admin-sidebar-hint">Console</div>

          <div className="admin-sidebar-links">
            <NavLink
              to="/admin/dashboard"
              className={({ isActive }) => (isActive ? "admin-sidebar-link active" : "admin-sidebar-link")}
            >
              Dashboard
            </NavLink>
            <NavLink
              to="/admin/users"
              className={({ isActive }) => (isActive ? "admin-sidebar-link active" : "admin-sidebar-link")}
            >
              Utilisateurs
            </NavLink>
          </div>
        </aside>

        <main className="admin-content">{children}</main>
      </div>

      <AdminFooter />
    </div>
  );
}

