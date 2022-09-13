<script>
    import Textfield from "@smui/textfield";
    import HelperText from "@smui/textfield/helper-text";
    import Button, { Label } from "@smui/button";
    import Icon from "@smui/textfield/icon";

    import { postForm } from "../lib/backend.js";
    import { getContext } from "svelte";
    import { state } from "../stores.js";

    let username = "";
    let password = "";
    let repassword = "";

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
        snackbar("Error during registration. Username may already be taken.");

        disabled = false;
    }

    let disabled = false;

    let re;

    // Re-enter Password field validation
    $: invalid = password !== repassword;
    $: if (re) re.getElement().setCustomValidity(invalid ? "Passwords do not match" : "");
</script>

<form action="/register/" on:submit|preventDefault={handleFormSubmit}>
    <div>
        <Textfield
            {disabled}
            bind:value={username}
            input$name="id"
            input$maxlength={20}
            input$pattern={"[A-Za-z0-9_]{3,20}"}
            input$title="3 to 20 characters. Only alphanumeric characters and underscores."
            input$spellcheck="false"
            required
            label="Username"
            variant="outlined"
        >
            <Icon class="material-symbols-rounded" slot="leadingIcon">person</Icon>
            <HelperText validationMsg slot="helper">
                {#if username.length >= 3}
                    Invalid characters
                {:else}
                    Username is too short
                {/if}
            </HelperText>
        </Textfield>
    </div>

    <div>
        <Textfield
            bind:value={password}
            input$name="password"
            label="Password"
            variant="outlined"
            type="password"
            input$pattern={".{3,80}"}
            input$title="3 to 80 characters."
            input$maxlength={80}
            required
            {disabled}
            updateInvalid
        >
            <Icon class="material-symbols-rounded" slot="leadingIcon">lock</Icon>
            <HelperText validationMsg slot="helper">Password is too short</HelperText>
        </Textfield>
    </div>
    <div>
        <Textfield
            bind:input={re}
            bind:value={repassword}
            input$name="password"
            label="Re-enter Password"
            variant="outlined"
            type="password"
            {disabled}
            required
            bind:invalid
        >
            <Icon class="material-symbols-rounded" slot="leadingIcon">lock</Icon>
            <HelperText validationMsg slot="helper">Passwords do not match</HelperText>
        </Textfield>

        <div>
            <Button {disabled} variant="raised" style="padding: 20px;">
                <Label>Register</Label>
            </Button>
        </div>
    </div>
</form>

<style>
    div {
        padding: 10px;
    }
</style>
