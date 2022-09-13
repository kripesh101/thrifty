const backend = import.meta.env.DEV
    ? window.location.origin + "/api"
    : "https://testsite.southeastasia.cloudapp.azure.com:3000";

export default backend;

export async function postForm(formEvent) {
    const form = formEvent.currentTarget;
    const formData = new FormData(form);
    const url = new URL(form.action);

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
