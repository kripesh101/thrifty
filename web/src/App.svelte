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
    {#if $state === "loggedout"}
        <RegisterForm />
    {:else if $state === "loggedin"}
        <Homepage />
    {:else if $state === "waiting"}
        <div>
            <CircularProgress style="height: 32px; width: 32px;" indeterminate />
        </div>
    {/if}
</main>
