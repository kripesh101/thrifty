<script>
    import Textfield from "@smui/textfield";
    import HelperText from "@smui/textfield/helper-text";
    import Button, { Label } from "@smui/button";
    import Snackbar, { Actions } from "@smui/snackbar";
    import IconButton from "@smui/icon-button";
    import Icon from "@smui/textfield/icon";

    import { postForm } from "../lib/backend.js";
    import { state } from "../stores.js";

    let username = "";
    let password = "";
    let invalid = null;

    async function handleFormSubmit(event) {
        disabled = true;

        const form = event.currentTarget;
        const formData = new FormData(form);
        const response = await postForm(form.action, formData);

        if (response.ok) {
            if ((await response.json()) === true) {
                disabled = false;
                $state = "loggedin";
                return;
            }
        }
        snackbarWithClose.open();

        disabled = false;
    }

    let disabled = false;
    let snackbarWithClose;
</script>

<Snackbar bind:this={snackbarWithClose} class="error">
    <Label>Error while logging in. Invalid username or password.</Label>
    <Actions>
        <IconButton class="material-symbols-rounded" title="Dismiss">close</IconButton>
    </Actions>
</Snackbar>

<form action="/login/" on:submit|preventDefault={handleFormSubmit}>
    <div>
        <Textfield
            bind:disabled
            bind:value={username}
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
            bind:invalid
            bind:disabled
            updateInvalid
        >
            <Icon class="material-symbols-rounded" slot="leadingIcon">lock</Icon>
            <HelperText validationMsg slot="helper">Password is too short</HelperText>
        </Textfield>
    </div>

    <Button bind:disabled variant="raised" style="padding: 20px;">
        <Label>Login</Label>
    </Button>
</form>

<style>
    div {
        padding: 10px;
    }
</style>
