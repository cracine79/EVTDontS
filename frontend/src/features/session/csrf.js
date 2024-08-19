async function csrfFetch(url, options = {}) {
  try {
    console.log('Making request to:', url);
    console.log('Request options:', options);

    options.headers ||= {};
    options.method ||= 'GET';

    if (options.method.toUpperCase() !== 'GET') {
      options.headers['Content-Type'] =
        options.headers['Content-Type'] || 'application/json';
      options.headers['X-CSRF-Token'] = sessionStorage.getItem('X-CSRF-Token');
    }
    // console.log(options)
    // console.log(url)
    // console.log('hello')
    const res = await fetch(url, options);

    console.log('Response status:', res.status);

    if (!res.ok) {
      const errorData = await res.json();
      console.error("Error response from server:", errorData);
      throw new Error(`Request failed with status ${res.status}`);
    }

    return res;
  } catch (err) {
    console.error("Fetch error:", err.message);
    console.error("Fetch error details:", err);
    throw err; // Re-throw the error to handle it in the calling function
  }
}

export function storeCSRFToken(response) {

    const csrfToken = response.headers.get("X-CSRF-Token");

    if (csrfToken) sessionStorage.setItem("X-CSRF-Token", csrfToken);
  }
  
  export async function restoreCSRF() {
    const response = await csrfFetch("/api/session");
    storeCSRFToken(response);
    return response;
  }

export default csrfFetch