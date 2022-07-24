const backend = import.meta.env.DEV
    ? "http://127.0.0.1:8000/"
    : "https://testsite.southeastasia.cloudapp.azure.com:3000/";

export default backend;
