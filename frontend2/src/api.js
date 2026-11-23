// fetch() for our API: adds the login token and turns error responses into thrown Errors
// (message format "HTTP error! Status: 401 - <server message>", which friendlyAuthError reads)
export async function apiFetch(url, options = {}) {
    options.method = options.method || 'GET';
    options.headers = options.headers || {};

    const authToken = localStorage.getItem('access_token')
    if (authToken && authToken !== 'null' && authToken !== 'undefined') {
        options.headers['Authorization'] = `Bearer ${authToken}`
    }

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            let errorMessage = `HTTP error! Status: ${response.status}`;
            try {
                const errorData = await response.json();
                errorMessage += ` - ${errorData.error || errorData.message || 'Unknown error'}`;
            } catch {
                // Not JSON
                errorMessage += ` - ${response.statusText}`;
            }
            throw new Error(errorMessage);
        }
        return response;
    } catch (error) {
        console.error('Fetch error:', error);
        throw error
    }
}
