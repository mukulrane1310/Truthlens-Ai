import { getToken } from '../utils/storage';

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export async function request(path, options = {}) {
  const token = getToken();

  const headers = {
    ...(options.body instanceof FormData
      ? {}
      : options.body
        ? { 'Content-Type': 'application/json' }
        : {}),
    ...options.headers,
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  let data = null;

  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    throw new Error(
      data?.detail || `Request failed with status ${response.status}`,
    );
  }

  return data;
}

export async function registerUser(email, password) {
  return request('/api/v1/auth/register', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
}

export async function loginUser(email, password) {
  return request('/api/v1/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
}

export async function getCurrentUser() {
  return request('/api/v1/auth/me');
}

export async function checkHealth() {
  try {
    return await request('/health');
  } catch (error) {
    console.error('Health check failed:', error);

    return {
      status: 'error',
      message: error.message || 'Failed to connect to backend server',
    };
  }
}
export async function getDashboardSummary() {
  return request('/api/v1/dashboard/summary');
}

export async function createClaim(claim_text) {
  return request('/api/v1/claims', {
    method: 'POST',
    body: JSON.stringify({ claim_text }),
  });
}

export async function getClaims(limit = 20, offset = 0) {
  const params = new URLSearchParams({
    limit: String(limit),
    offset: String(offset),
  });

  return request(`/api/v1/claims?${params.toString()}`);
}

export async function getClaimById(claimId) {
  return request(`/api/v1/claims/${claimId}`);
}

export async function collectClaimEvidence(claimId, query, max_results = 5) {
  return request(`/api/v1/evidence/collect/${claimId}`, {
    method: 'POST',
    body: JSON.stringify({ query, max_results }),
  });
}

export async function getClaimEvidence(claimId) {
  return request(`/api/v1/evidence/${claimId}`);
}
export async function getUploadedClaimEvidence(claimId) {
  return request(`/api/v1/evidence/${claimId}/uploaded`);
}

export async function analyzeClaim(claimId) {
  return request(`/api/v1/analysis/${claimId}`, {
    method: 'POST',
  });
}

export async function getClaimAnalysis(claimId) {
  return request(`/api/v1/analysis/${claimId}`);
}
export async function uploadClaimDocument(claimId, file) {
  const formData = new FormData();
  formData.append('file', file);

  return request(`/api/v1/uploads/${claimId}/document`, {
    method: 'POST',
    body: formData,
  });
}

export async function uploadClaimImage(claimId, file) {
  const formData = new FormData();
  formData.append('file', file);

  return request(`/api/v1/uploads/${claimId}/image`, {
    method: 'POST',
    body: formData,
  });
}
export async function sendChatMessage(claimId, message) {
  return request(`/api/v1/chat/${claimId}`, {
    method: 'POST',
    body: JSON.stringify({ message }),
  });
}

export async function getChatHistory(claimId) {
  return request(`/api/v1/chat/${claimId}`);
}