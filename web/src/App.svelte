<script>
    import Snackbar, { Actions, Label } from "@smui/snackbar";
    import IconButton from "@smui/icon-button";
    import CircularProgress from "@smui/circular-progress";
    import Homepage from "./pages/Homepage.svelte";
    import RegisterForm from "./pages/LandingPage.svelte";
    import fetchBackend from "./lib/backend.js";
    import { onMount, setContext } from "svelte";
    import { state } from "./stores.js";

    // waiting | not_loggedin | loggedin
    $state = "waiting";

    onMount(async () => {
        const res = await fetchBackend("/is_logged_in/");
        if (res.ok) {
            if ((await res.json()) == true) {
                $state = "loggedin";
                return;
            }
        }
        $state = "loggedout";
    });

    let snackbar, snackbarText, snackbarClass;

    setContext("snackbar", async (msg, classes = "error") => {
        // Close current snackbar (if open)
        snackbar.close();

        // Only close snackbar if empty msg
        if (msg === "") return;

        // Wait 0.05s (for closing animation)
        await new Promise((r) => setTimeout(r, 50));

        // Update props
        snackbarText = msg;
        snackbarClass = classes;

        // Open snackbar
        snackbar.open();
    });
</script>

<main>
    <Snackbar bind:this={snackbar} class={snackbarClass}>
        <Label>{snackbarText}</Label>
        <Actions>
            <IconButton class="material-symbols-rounded" title="Dismiss">close</IconButton>
        </Actions>
    </Snackbar>

    {#if $state === "loggedin"}
        <Homepage />
    {:else}
        <div class="container">
            <div class="item">
                {#if $state === "loggedout"}
                    <RegisterForm />
                {:else if $state === "waiting"}
                    <CircularProgress style="height: 32px; width: 32px;" indeterminate />
                {/if}
            </div>
        </div>
    {/if}
</main>

<style>
    .container {
        display: flex;
        place-items: center;
        min-width: 320px;
        min-height: 100vh;
    }

    .item {
        margin: 0 auto;
    }
</style>
