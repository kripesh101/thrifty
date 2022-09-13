<script>
    import Textfield from "@smui/textfield";
    import HelperText from "@smui/textfield/helper-text";
    import Button, { Label } from "@smui/button";
    import Icon from "@smui/textfield/icon";

    import { getContext } from "svelte";
    import { postForm } from "../lib/backend.js";
    import { state } from "../stores.js";

    let username = "";
    let password = "";

    const snackbar = getContext("snackbar");

    async function handleFormSubmit(event) {
        disabled = true;

        const response = await postForm(event);

        if (response.ok) {
            if ((await response.json()) === true) {
                snackbar("");
                disabled = false;
                $state = "loggedin";
                return;
            }
        }
        snackbar("Error while logging in. Invalid username or password.");

        disabled = false;
    }

    let disabled = false;
</script>

<form action="/login/" on:submit|preventDefault={handleFormSubmit}>
    <div>
        <Textfield
            bind:value={username}
            {disabled}
            input$name="id"
            label="Username"
            variant="outlined"
        >
            <Icon class="material-symbols-rounded" slot="leadingIcon">person</Icon>
        </Textfield>
    </div>

    <div>
        <Textfield
            bind:value={password}
            input$name="password"
            label="Password"
            variant="outlined"
            type="password"
            {disabled}
        >
            <Icon class="material-symbols-rounded" slot="leadingIcon">lock</Icon>
            <HelperText validationMsg slot="helper">Password is too short</HelperText>
        </Textfield>
    </div>

    <Button {disabled} variant="raised" style="padding: 20px;">
        <Label>Login</Label>
    </Button>
</form>

<style>
    div {
        padding: 10px;
    }
</style>
