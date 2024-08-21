export async function csrfFetch(url, options = {}) {
  options.method = options.method || 'GET';
  options.headers = options.headers || {};

  // Fetch CSRF token if not present in options
  if (options.method.toUpperCase() !== 'GET') {
    const token = sessionStorage.getItem('X-CSRF-TOKEN');
    if (token) {
      options.headers['X-CSRF-TOKEN'] = token;
    }
    options.headers['Content-Type'] = 'application/json';
  }

  const response = await fetch(url, options);

  // Automatically store the CSRF token from the response if available
  if (response.headers.has('X-CSRF-TOKEN')) {
    const token = response.headers.get('X-CSRF-TOKEN');
    sessionStorage.setItem('X-CSRF-TOKEN', token);
  }

  return response;
}

// export function storeCSRFToken(response) {

//     const csrfToken = response.headers.get("X-CSRF-Token");

//     if (csrfToken) sessionStorage.setItem("X-CSRF-Token", csrfToken);
//   }
  
//   export async function restoreCSRF() {
//     const response = await csrfFetch("/api/session");
//     storeCSRFToken(response);
//     return response;
//   }

// export default csrfFetch