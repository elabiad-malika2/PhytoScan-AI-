import { useEffect, useState } from "react";
import { api } from "../api";

export default function AdminUsers() {
  const [users, setUsers] = useState([]);

  const loadUsers = () => api.getAdminUsers().then(setUsers).catch(console.error);

  useEffect(() => { loadUsers(); }, []);

  const handleDelete = async (id, username) => {
    if (window.confirm(`Supprimer l'agriculteur ${username} et toutes ses données ?`)) {
      await api.deleteUser(id);
      loadUsers(); // Rafraîchit la liste
    }
  };

  return (
    <div className="container">
      <div className="page-head">
        <div className="page-kicker">
          <span className="pill">🛡 Admin</span>
          <span className="pill">👥 Utilisateurs</span>
        </div>
        <h2 className="h2">Gestion des agriculteurs</h2>
        <p className="p" style={{ fontSize: 14 }}>
          Consultez les comptes créés et supprimez, si nécessaire, les utilisateurs et leurs données
          associées.
        </p>
      </div>

      <div className="card admin-table">
        <div className="admin-table-head">
          <span className="label">Liste des utilisateurs</span>
          <span className="pill">Total : {users.length}</span>
        </div>

        <div className="admin-table-body">
          <div className="admin-table-row admin-table-row--header">
            <div className="admin-col-id">ID</div>
            <div className="admin-col-name">Nom</div>
            <div className="admin-col-email">Email</div>
            <div className="admin-col-actions">Action</div>
          </div>

          {users.map((u) => (
            <div key={u.id} className="admin-table-row">
              <div className="admin-col-id">
                <span className="admin-badge-id">#{u.id}</span>
              </div>
              <div className="admin-col-name">
                <div style={{ fontWeight: 600 }}>{u.username}</div>
              </div>
              <div className="admin-col-email">
                <span style={{ fontSize: 13 }}>{u.email}</span>
              </div>
              <div className="admin-col-actions">
                <button
                  type="button"
                  className="btn admin-btn-danger"
                  onClick={() => handleDelete(u.id, u.username)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}

          {users.length === 0 && (
            <div className="admin-table-row">
              <div className="admin-col-empty">
                <p className="p">Aucun utilisateur trouvé pour le moment.</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}