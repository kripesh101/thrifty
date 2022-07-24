<script>
    import backend from "./backend";

    async function getAPI() {
        const res = await fetch(backend);
        const text = await res.text();

        if (res.ok) return text;
        else throw new Error(text);
    }

    const promise = getAPI();
</script>

{#await promise}
    <p>...waiting</p>
{:then res}
    <p>The result is {res}</p>
{:catch error}
    <p style="color: red">{error.message}</p>
{/await}
