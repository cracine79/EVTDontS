export async function csrfFetch(url, options = {}) {
    options.method = options.method || 'GET';
    options.headers = options.headers || {};
  
    // Set the CSRF token if the method is not GET
    if (options.method !== 'GET') {
      const token = sessionStorage.getItem('X-CSRF-Token');
      options.headers['X-CSRF-Token'] = token;
    }
  
    const response = await fetch(url, options);
  
    if (response.ok) {
      return response;
    } else {
      throw new Error('Failed to fetch');
    }
  }
  
  // Get CSRF token when app starts
  export async function restoreCSRF() {
    const response = await fetch('/api/csrf');
    const { csrf_token } = await response.json();
    sessionStorage.setItem('X-CSRF-Token', csrf_token);
  }