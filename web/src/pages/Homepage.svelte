<script>
    import Button, { Label } from "@smui/button";
    import { state } from "../stores.js";
    import backend from "../lib/backend";
</script>

<Button
    variant="raised"
    style="padding: 30px;"
    on:click={async () => {
        const res = await fetch(backend + "/logout/", {
            method: "POST",
            credentials: "include",
            mode: "cors"
        });
        if ((await res.json()).success) {
            $state = "loggedout";
        }
    }}
>
    <Label>Log out</Label>
</Button>
