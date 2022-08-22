<script>
    import Textfield from "@smui/textfield";
    import HelperText from "@smui/textfield/helper-text";
    import Button, { Label } from "@smui/button";
    import Snackbar, { Actions } from "@smui/snackbar";
    import IconButton from "@smui/icon-button";
    import Icon from "@smui/textfield/icon";

    import { postForm } from "../lib/backend.js";
    import { onMount } from "svelte";
    import { state } from "../stores.js";

    let username = "";
    let password = "";
    let repassword = "";

    async function handleFormSubmit(event) {
        disabled = true;

        event.preventDefault();
        const form = event.currentTarget;
        const formData = new FormData(form);
        const response = await postForm(form.action, formData);

        if (response.ok) {
            if ((await response.json()).success) {
                disabled = false;
                $state = "loggedin";
                return;
            }
        }
        snackbar.open();

        disabled = false;
    }

    let disabled = false;
    let snackbar;

    let re;
    let mounted = false;

    onMount(() => {
        mounted = true;
    });

    // Re-enter Password field validation
    $: invalid = password !== repassword;
    $: if (mounted) {
        re.getElement().setCustomValidity(invalid ? "Passwords do not match" : "");
    }
</script>

<Snackbar bind:this={snackbar} class="error">
    <Label>Error during registration. Username may already be taken.</Label>
    <Actions>
        <IconButton class="material-symbols-rounded" title="Dismiss">close</IconButton>
    </Actions>
</Snackbar>

<form action="/register/" on:submit={handleFormSubmit}>
    <div>
        <Textfield
            bind:disabled
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
            bind:disabled
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
            bind:disabled
            required
            bind:invalid
        >
            <Icon class="material-symbols-rounded" slot="leadingIcon">lock</Icon>
            <HelperText validationMsg slot="helper">Passwords do not match</HelperText>
        </Textfield>

        <div>
            <Button bind:disabled variant="raised" style="padding: 20px;">
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
