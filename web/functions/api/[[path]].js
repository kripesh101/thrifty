export async function onRequest({ request }) {
    const url = new URL(request.url);
    url.hostname = "testsite.southeastasia.cloudapp.azure.com";
    url.protocol = "http:";
    url.pathname = url.pathname.slice(url.pathname.indexOf("/", 1));
    url.port = "";
    return fetch(url.toString(), request);
}
