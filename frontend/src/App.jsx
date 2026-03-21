import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
  useLocation,
} from "react-router-dom";
import { useState } from "react";
import Header from "./components/Header";
import Footer from "./components/Footer";
import AdminLayout from "./components/AdminLayout";
import Home from "./pages/Home";
import About from "./pages/About";
import Sign from "./pages/Sign";
import Login from "./pages/Login";
import ScanPage from "./pages/ScanPage";
import ChatPage from "./pages/ChatPage";
import HistoryPage from "./pages/HistoryPage";
import AdminDashboard from "./pages/AdminDashboard";
import AdminUsers from "./pages/AdminUsers";

function App() {
  // On vérifie si un token existe au démarrage
  const [token, setToken] = useState(localStorage.getItem("token"));
  const role = localStorage.getItem("role");

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <Router>
      <AppInner
        token={token}
        setToken={setToken}
        role={role}
        onLogout={handleLogout}
      />
    </Router>
  );
}

function AppInner({ token, setToken, role, onLogout }) {
  const location = useLocation();
  const isAdminRoute = location.pathname.startsWith("/admin");

  return (
    <div className="app-shell">
      {!isAdminRoute && <Header token={token} onLogout={onLogout} />}

      <main className={isAdminRoute ? "" : "app-main"}>
        <Routes>
          {/* Public */}
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route
            path="/login"
            element={
              token ? (role === "admin" ? (<Navigate to="/admin/dashboard" />) : (<Navigate to="/diagnostic" />)
              ) : (
                <Login setToken={setToken} />
              )
            }
          />
          <Route
            path="/sign"
            element={token && role === "agriculteur" ? <Navigate to="/diagnostic" /> : <Sign />}
          />

          {/* Private */}
          <Route
            path="/diagnostic"
            element={token && role === "agriculteur" ? <ScanPage /> : <Navigate to="/login" />}
          />
          <Route
            path="/assistant"
            element={token && role === "agriculteur" ? <ChatPage /> : <Navigate to="/login" />}
          />
          <Route
            path="/history"
            element={token && role === "agriculteur" ? <HistoryPage /> : <Navigate to="/login" />}
          />

          {/* Admin */}
          <Route
            path="/admin/dashboard"
            element={
              token && role === "admin" ? (
                <AdminLayout onLogout={onLogout}>
                  <AdminDashboard />
                </AdminLayout>
              ) : (
                <Navigate to="/login" />
              )
            }
          />
          <Route
            path="/admin/users"
            element={
              token && role === "admin" ? (
                <AdminLayout onLogout={onLogout}>
                  <AdminUsers />
                </AdminLayout>
              ) : (
                <Navigate to="/login" />
              )
            }
          />

          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </main>

      {!isAdminRoute && <Footer />}
    </div>
  );
}
export default App;
