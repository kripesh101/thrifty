export const backendRoot = window.location.origin + "/api";

export function postForm(formEvent, method = "post", pathname) {
    const form = formEvent.currentTarget;
    const formData = new FormData(form);
    if (!pathname) {
        const url = new URL(form.action);
        pathname = url.pathname;
    }

    const plainFormData = Object.fromEntries(formData.entries());
    const response = fetchBackend(pathname, method, plainFormData);
    return response;
}

export default function fetchBackend(path, method, body) {
    if (typeof body !== "string") body = JSON.stringify(body);

    return fetch(backendRoot + path, {
        method,
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json"
        },
        credentials: "include",
        body
    });
}
