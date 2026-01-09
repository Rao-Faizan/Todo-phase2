// API Client for interacting with the backend API

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

interface SignupData {
  email: string;
  password: string;
}

interface LoginData {
  email: string;
  password: string;
}

interface TaskData {
  title: string;
  description?: string;
  completed?: boolean;
}

interface ApiResponse<T> {
  data: T;
  error?: string;
}

// Helper function to get auth token
const getAuthToken = () => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('authToken');
  }
  return null;
};

// Helper function to get user ID from token
const getUserIdFromToken = () => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('authToken');
    if (token) {
      try {
        const base64Url = token.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(
          atob(base64)
            .split('')
            .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
            .join('')
        );

        const decoded = JSON.parse(jsonPayload);
        return decoded.sub; // sub field typically contains user ID
      } catch (error) {
        console.error('Error decoding JWT:', error);
        return null;
      }
    }
  }
  return null;
};

// Helper function to make API requests
const makeRequest = async <T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> => {
  const url = `${API_BASE_URL}${endpoint}`;

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Add auth token if available
  const authToken = getAuthToken();
  if (authToken) {
    (headers as any)['Authorization'] = `Bearer ${authToken}`;
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }

  return response.json();
};

// Authentication functions
export const signupUser = async (userData: SignupData) => {
  return makeRequest('/api/auth/signup', {
    method: 'POST',
    body: JSON.stringify(userData),
  });
};

export const loginUser = async (loginData: LoginData) => {
  return makeRequest('/api/auth/signin', {
    method: 'POST',
    body: JSON.stringify(loginData),
  });
};

// Task functions
export const getUserTasks = async () => {
  const userId = getUserIdFromToken();
  if (!userId) {
    throw new Error('User not authenticated');
  }
  return makeRequest(`/api/${userId}/tasks`);
};

export const createTask = async (taskData: TaskData) => {
  const userId = getUserIdFromToken();
  if (!userId) {
    throw new Error('User not authenticated');
  }
  return makeRequest(`/api/${userId}/tasks`, {
    method: 'POST',
    body: JSON.stringify(taskData),
  });
};

export const getTask = async (taskId: string) => {
  const userId = getUserIdFromToken();
  if (!userId) {
    throw new Error('User not authenticated');
  }
  return makeRequest(`/api/${userId}/tasks/${taskId}`);
};

export const updateTask = async (taskId: string, taskData: Partial<TaskData>) => {
  const userId = getUserIdFromToken();
  if (!userId) {
    throw new Error('User not authenticated');
  }
  return makeRequest(`/api/${userId}/tasks/${taskId}`, {
    method: 'PUT',
    body: JSON.stringify(taskData),
  });
};

export const toggleTaskCompletion = async (taskId: string, completed: boolean) => {
  const userId = getUserIdFromToken();
  if (!userId) {
    throw new Error('User not authenticated');
  }
  return makeRequest(`/api/${userId}/tasks/${taskId}/complete`, {
    method: 'PATCH',
    body: JSON.stringify({ completed }),
  });
};

export const deleteTask = async (taskId: string) => {
  const userId = getUserIdFromToken();
  if (!userId) {
    throw new Error('User not authenticated');
  }
  return makeRequest(`/api/${userId}/tasks/${taskId}`, {
    method: 'DELETE',
  });
};