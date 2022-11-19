<script>
    import Paper from "@smui/paper";
    import { onMount } from "svelte";
    import Expense from "@/lib/Expense.svelte";
    import fetchBackend from "@/lib/backend";

    let expenses;

    export async function refresh(visible = true, callback) {
        if (visible) expenses = "loading";
        const res = await fetchBackend("/expenses/");
        expenses = await res.json();
        callback?.();
    }

    onMount(refresh);
</script>

<Paper>
    <h6 style="line-height: 1.6; text-align: left; margin: auto; font-weight: 600;">History</h6>
    {#if expenses instanceof Array}
        <!-- Loaded content from server -->
        {#each expenses as data}
            <Expense {data} />
        {:else}
            <p><i>No entries.</i></p>
        {/each}
    {:else}
        <p>Loading...</p>
    {/if}
</Paper>

<style>
</style>
