// Utility functions for authentication

// Function to decode JWT token
export const decodeJWT = (token: string) => {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );

    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error('Error decoding JWT:', error);
    return null;
  }
};

// Function to get user ID from JWT token
export const getUserIdFromToken = (): string | null => {
  if (typeof window === 'undefined') {
    return null; // Not in browser
  }

  const token = localStorage.getItem('authToken');
  if (!token) {
    return null;
  }

  const decoded = decodeJWT(token);
  if (decoded && decoded.sub) {
    return decoded.sub; // sub field typically contains user ID
  }

  return null;
};

// Function to check if token is expired
export const isTokenExpired = (token: string): boolean => {
  const decoded = decodeJWT(token);
  if (!decoded || !decoded.exp) {
    return true; // If no exp claim, consider expired
  }

  const currentTime = Math.floor(Date.now() / 1000);
  return decoded.exp < currentTime;
};

// Function to get token expiration
export const getTokenExpiration = (token: string): Date | null => {
  const decoded = decodeJWT(token);
  if (!decoded || !decoded.exp) {
    return null;
  }

  return new Date(decoded.exp * 1000);
};