const backend = import.meta.env.DEV
    ? "http://127.0.0.1:8000/"
    : "http://testsite.southeastasia.cloudapp.azure.com/";

export default backend;
