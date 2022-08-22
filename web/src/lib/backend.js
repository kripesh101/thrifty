let backend;
if (import.meta.env.DEV) {
    const url = new URL(window.location.href);
    url.port = "8000";
    url.pathname = "";
    backend = url.origin;
} else {
    backend = "https://testsite.southeastasia.cloudapp.azure.com:3000";
}

export default backend;

export async function postForm(target, formData) {
    const url = new URL(target);

    const plainFormData = Object.fromEntries(formData.entries());
    const formDataJsonString = JSON.stringify(plainFormData);
    const response = await fetch(backend + url.pathname, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json"
        },
        credentials: "include",
        body: formDataJsonString
    });

    return response;
}
