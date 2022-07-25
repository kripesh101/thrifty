let backend;
if (import.meta.env.DEV) {
    const url = new URL(window.location.href);
    url.port = "8000";
    url.pathname = "";
    backend = url.origin;
} else {
    backend = "https://testsite.southeastasia.cloudapp.azure.com:3000/";
}

export default backend;
