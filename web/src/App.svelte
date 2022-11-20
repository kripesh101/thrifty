<script>
    import Router from "svelte-spa-router";
    import Snackbar, { Actions, Label } from "@smui/snackbar";
    import IconButton from "@smui/icon-button";
    import CircularProgress from "@smui/circular-progress";
    import { onMount, setContext } from "svelte";
    import { state } from "./stores.js";
    import fetchBackend from "./lib/backend.js";

    import Landing from "./pages/landing/Landing.svelte";
    import CredentialsForm from "./pages/credentials/CredentialsForm.svelte";
    import Dashboard from "./pages/dashboard/Dashboard.svelte";
    import Logo from "./lib/Logo.svelte";

    const loggedoutRoutes = {
        "/": Landing,
        "/start": CredentialsForm,
        "*": Landing
    };

    // waiting | loggedout | loggedin
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
        <Dashboard />
    {:else if $state === "loggedout"}
        <Router routes={loggedoutRoutes} />
    {:else if $state === "waiting"}
        <div class="container">
            <div class="item">
                <div>
                    <Logo />
                    <br />
                    <CircularProgress style="height: 32px; width: 32px;" indeterminate />
                </div>
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
