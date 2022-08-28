<script>
    import Homepage from "./pages/Homepage.svelte";
    import RegisterForm from "./pages/LandingPage.svelte";
    import CircularProgress from "@smui/circular-progress";
    import { onMount } from "svelte";
    import backend from "./lib/backend.js";
    import { state } from "./stores.js";

    // waiting | not_loggedin | loggedin
    $state = "waiting";

    onMount(async () => {
        const res = await fetch(backend + "/is_logged_in/", {
            credentials: "include",
            mode: "cors"
        });
        if (res.ok) {
            if ((await res.json()) == true) {
                $state = "loggedin";
                return;
            }
        }
        $state = "loggedout";
    });
</script>

<main>
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
