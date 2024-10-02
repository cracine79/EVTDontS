export async function csrfFetch(url, options = {}) {
    options.method = options.method || 'GET';
    options.headers = options.headers || {};
  
    // Set the CSRF token if the method is not GET
    if (options.method != 'GET') {
        
        const token = sessionStorage.getItem('X-CSRF-Token');
        
        if(token){
            options.headers['X-CSRF-Token'] = token;
        } else {
            console.warn('No CSRF token found in sessionStorage.');
        }
    }
    const auth_token = localStorage.getItem('access_token')
    if(auth_token){
        options.headers['Authorization'] = `Bearer ${auth_token}`
    }

    try{
        
        const response = await fetch(url, options);
        if (!response.ok){
               // Try to parse JSON response if available
                let errorMessage = `HTTP error! Status: ${response.status}`;
                try {
                    const errorData = await response.json();
                    errorMessage += ` - ${errorData.error || errorData.message || 'Unknown error'}`;
                } catch (e) {
                    // Handle the case where response is not JSON
                    errorMessage += ` - ${response.statusText}`;
                }
                throw new Error(errorMessage);
        }
        return response;
        }catch(error){
            console.error('Fetch error:', error);
            throw error
        }
    }
  
  
  // Get CSRF token when app starts
  export async function restoreCSRF() {
    const response = await fetch('/api/csrf');
    const { csrf_token } = await response.json();
    sessionStorage.setItem('X-CSRF-Token', csrf_token);
  }