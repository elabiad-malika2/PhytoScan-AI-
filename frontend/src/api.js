const BASE_URL = "http://localhost:8000/api/v1";

// Fonction pour récupérer le token sauvegardé
const getToken = () => localStorage.getItem("token");

export const api = {
  // 1. LOGIN (FastAPI exige le format URL Encoded pour le login !)
  login: async (email, password) => {
    const formData = new URLSearchParams();
    formData.append("username", email); // FastAPI utilise "username" par défaut
    formData.append("password", password);

    const response = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData,
    });
    if (!response.ok) throw new Error("Erreur de connexion");
    return response.json();
  },

  // 2. SCAN (Envoi d'image en FormData)
  analyzeScan: async (file) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("langue", "fr");

    const response = await fetch(`${BASE_URL}/scans/analyze`, {
      method: "POST",
      headers: { Authorization: `Bearer ${getToken()}` }, // Pas de Content-Type ici, le navigateur le gère avec FormData !
      body: formData,
    });
    if (!response.ok) throw new Error("Erreur lors de l'analyse");
    return response.json();
  },

  // 3. CHAT (Envoi de texte en JSON)
  askChatbot: async (question) => {
    const response = await fetch(`${BASE_URL}/chat/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${getToken()}`,
      },
      body: JSON.stringify({ question, langue: "fr" }),
    });
    if (!response.ok) throw new Error("Erreur du chatbot");
    return response.json();
  },
  // 4. INSCRIPTION (Register)
  register: async (username, email, password) => {
    const response = await fetch(`${BASE_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password, role: "agriculteur" }),
    });
    if (!response.ok) throw new Error("Erreur lors de l'inscription (Email peut-être déjà utilisé)");
    return response.json();
  },

  // 5. HISTORIQUE DES SCANS & RAPPORTS
  getScanHistory: async () => {
    const response = await fetch(`${BASE_URL}/reports/history`, {
      method: "GET",
      headers: { Authorization: `Bearer ${getToken()}` },
    });
    if (!response.ok) throw new Error("Erreur lors de la récupération des scans");
    return response.json();
  },

  // 6. HISTORIQUE DU CHATBOT
  getChatHistory: async () => {
    const response = await fetch(`${BASE_URL}/chat/history`, {
      method: "GET",
      headers: { Authorization: `Bearer ${getToken()}` },
    });
    if (!response.ok) throw new Error("Erreur lors de la récupération du chat");
    return response.json();
  },
   // 7. TÉLÉCHARGER LE PDF (Renvoie un Blob au lieu de JSON)
  downloadReport: async (scanId) => {
    const response = await fetch(`${BASE_URL}/reports/download/${scanId}`, {
      method: "GET",
      headers: { Authorization: `Bearer ${getToken()}` },
    });
    
    if (!response.ok) throw new Error("Erreur lors du téléchargement du PDF");
    
    // TRÈS IMPORTANT : On retourne un Blob (Fichier binaire) et non un JSON !
    return response.blob();
  },

  // ==========================================
  // ROUTES ADMIN
  // ==========================================
  getAdminDashboard: async () => {
    const response = await fetch(`${BASE_URL}/admin/dashboard`, {
      headers: { Authorization: `Bearer ${getToken()}` },
    });
    if (!response.ok) throw new Error("Accès refusé");
    return response.json();
  },

  getAdminUsers: async () => {
    const response = await fetch(`${BASE_URL}/admin/users`, {
      headers: { Authorization: `Bearer ${getToken()}` },
    });
    if (!response.ok) throw new Error("Accès refusé");
    return response.json();
  },

  deleteUser: async (userId) => {
    const response = await fetch(`${BASE_URL}/admin/users/${userId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${getToken()}` },
    });
    if (!response.ok) throw new Error("Erreur lors de la suppression");
    return response.json();
  }

};

