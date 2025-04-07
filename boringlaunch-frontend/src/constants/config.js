export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const ROUTES = {
  HOME: '/',
  DASHBOARD: '/dashboard',
  STARTUPS: {
    LIST: '/startups',
    NEW: '/startups/new',
    EDIT: (id) => `/startups/${id}/edit`,
    DETAIL: (id) => `/startups/${id}`,
  },
  PLATFORMS: {
    LIST: '/platforms',
    UPLOAD: '/platforms/upload',
  },
  SUBMISSIONS: {
    LIST: '/submissions',
    DETAIL: (id) => `/submissions/${id}`,
  },
};

export const SUBMISSION_STATUS = {
  PENDING: 'pending',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  FAILED: 'failed',
};

export const STATUS_COLORS = {
  [SUBMISSION_STATUS.PENDING]: 'bg-yellow-100 text-yellow-800',
  [SUBMISSION_STATUS.IN_PROGRESS]: 'bg-blue-100 text-blue-800',
  [SUBMISSION_STATUS.COMPLETED]: 'bg-green-100 text-green-800',
  [SUBMISSION_STATUS.FAILED]: 'bg-red-100 text-red-800',
};

export const TABLE_PAGE_SIZES = [10, 25, 50, 100];

export const DATE_FORMAT = 'MMMM DD, YYYY HH:mm:ss';

export const TOAST_DURATION = 5000; // 5 seconds

export const API_ENDPOINTS = {
  STARTUPS: '/api/startups',
  PLATFORMS: '/api/platforms',
  SUBMISSIONS: '/api/submissions',
};

export const VALIDATION = {
  URL_PATTERN: /^https?:\/\/.+/,
  MAX_NAME_LENGTH: 100,
  MAX_DESCRIPTION_LENGTH: 500,
};

export const FILE_UPLOAD = {
  ACCEPTED_TYPES: '.xlsx,.xls',
  MAX_SIZE: 5 * 1024 * 1024, // 5MB
}; 