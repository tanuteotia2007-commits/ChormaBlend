// ============================================================================
// src/services/api.js
//
// Single centralized API layer. No component should call fetch() directly —
// everything goes through the functions exported here. This is the ONLY file
// that needs to change if the backend contract changes.
//
// Contract source of truth: /API_CONTRACT.md (repo root)
// ============================================================================

// In dev, Vite proxies "/api" to the Flask backend (see vite.config.js), so a
// relative path works both in dev and once built/served behind the same host.
const BASE_URL = '/api';

/**
 * Thin wrapper around fetch that:
 * - always sends/receives JSON (unless isFormData is set)
 * - always includes credentials so the Flask session cookie is sent
 * - normalizes errors into a consistent shape the UI can render
 */
async function request(path, { method = 'GET', body, isFormData = false } = {}) {
  const options = {
    method,
    credentials: 'include', // required so Flask session cookie is sent/stored
  };

  if (body !== undefined) {
    if (isFormData) {
      options.body = body; // browser sets multipart headers automatically
    } else {
      options.headers = { 'Content-Type': 'application/json' };
      options.body = JSON.stringify(body);
    }
  }

  let response;
  try {
    response = await fetch(`${BASE_URL}${path}`, options);
  } catch (networkErr) {
    // Backend unreachable / offline / CORS hard-failure
    const err = new Error('Could not reach the server. Check your connection.');
    err.isNetworkError = true;
    throw err;
  }

  let data = null;
  try {
    data = await response.json();
  } catch {
    // Non-JSON response body (e.g. a raw 500 HTML page) — keep data null.
  }

  if (!response.ok) {
    const message =
      (data && data.message) ||
      `Request failed (${response.status})`;
    const err = new Error(message);
    err.status = response.status;
    err.data = data;
    throw err;
  }

  return data;
}

// --------------------------------------------------------------------------
// AUTH — hidden Safety Dashboard access
// --------------------------------------------------------------------------
export const authAPI = {
  unlock: (passcode) =>
    request('/auth/unlock', { method: 'POST', body: { passcode } }),

  status: () => request('/auth/status', { method: 'GET' }),

  exit: () => request('/auth/exit', { method: 'POST' }),
};

// --------------------------------------------------------------------------
// PRODUCTIVITY — Notes / To-Do / Planner (visible, disguise layer)
// --------------------------------------------------------------------------
export const productivityAPI = {
  // Notes
  getNotes: () => request('/notes', { method: 'GET' }),
  createNote: (note) => request('/notes', { method: 'POST', body: note }),
  updateNote: (noteId, note) =>
    request(`/notes/${noteId}`, { method: 'PUT', body: note }),
  deleteNote: (noteId) => request(`/notes/${noteId}`, { method: 'DELETE' }),

  // To-Do
  getTodos: () => request('/todos', { method: 'GET' }),
  createTodo: (todo) => request('/todos', { method: 'POST', body: todo }),
  updateTodo: (todoId, todo) =>
    request(`/todos/${todoId}`, { method: 'PUT', body: todo }),
  deleteTodo: (todoId) => request(`/todos/${todoId}`, { method: 'DELETE' }),

  // Planner
  getPlanner: () => request('/planner', { method: 'GET' }),
  createPlannerItem: (item) =>
    request('/planner', { method: 'POST', body: item }),
  updatePlannerItem: (itemId, item) =>
    request(`/planner/${itemId}`, { method: 'PUT', body: item }),
  deletePlannerItem: (itemId) =>
    request(`/planner/${itemId}`, { method: 'DELETE' }),
};

// --------------------------------------------------------------------------
// AI — Safety Planner (frontend never talks to Gemini directly)
// --------------------------------------------------------------------------
export const aiAPI = {
  getSafetyPlan: ({ situation, urgency, location_context, preferences }) =>
    request('/ai/safety-plan', {
      method: 'POST',
      body: { situation, urgency, location_context, preferences },
    }),
};

// --------------------------------------------------------------------------
// DOCUMENTS — Secure Document Vault
// --------------------------------------------------------------------------
export const documentsAPI = {
  list: () => request('/documents', { method: 'GET' }),

  upload: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return request('/documents', {
      method: 'POST',
      body: formData,
      isFormData: true,
    });
  },

  remove: (documentId) =>
    request(`/documents/${documentId}`, { method: 'DELETE' }),

  downloadUrl: (documentId) => `${BASE_URL}/documents/${documentId}/download`,
};

// --------------------------------------------------------------------------
// CONTACTS — trusted emergency contacts
// --------------------------------------------------------------------------
export const contactsAPI = {
  list: () => request('/contacts', { method: 'GET' }),
  add: (contact) => request('/contacts', { method: 'POST', body: contact }),
  update: (contactId, contact) =>
    request(`/contacts/${contactId}`, { method: 'PUT', body: contact }),
  remove: (contactId) =>
    request(`/contacts/${contactId}`, { method: 'DELETE' }),
};

// --------------------------------------------------------------------------
// EMERGENCY — SOS workflow
// --------------------------------------------------------------------------
export const emergencyAPI = {
  sendSOS: (contactIds) =>
    request('/emergency/sos', {
      method: 'POST',
      body: { contact_ids: contactIds },
    }),
};
