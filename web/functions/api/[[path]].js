export async function onRequest({ request, params }) {
    return fetch(`http://testsite.southeastasia.cloudapp.azure.com/${params.path}`, request);
}
