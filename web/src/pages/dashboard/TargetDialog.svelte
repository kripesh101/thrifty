<script>
    import Dialog, { Header, Title, Content, Actions } from "@smui/dialog";
    import Button, { Label } from "@smui/button";
    import Textfield from "@smui/textfield";
    import HelperText from "@smui/textfield/helper-text";
    import Icon from "@smui/textfield/icon";
    import { getContext } from "svelte";

    import fetchBackend from "@/lib/backend";

    export let open;

    let disabled = false;
    let target = "";

    async function loadData() {
        target = "";
        disabled = true;
        const res = await fetchBackend("/settings/weekly_target/");
        target = await res.json();
        disabled = false;
    }

    const snackbar = getContext("snackbar");
    const refresh = getContext("refresh");

    async function handleFormSubmit() {
        // "Confirm" button clicked
        disabled = true;

        const response = await fetchBackend(`/settings/weekly_target/${target}`, "PATCH");

        if (response.ok && (await response.json()) === true) {
            snackbar("Updated weekly target.", "success");
            refresh();
            open = false;
        } else {
            snackbar("Error updating weekly target. Please try again.");
        }

        disabled = false;
    }
</script>

<form on:submit|preventDefault={handleFormSubmit}>
    <Dialog
        bind:open
        aria-labelledby="title"
        aria-describedby="content"
        on:SMUIDialog:opening={loadData}
        scrimClickAction={disabled ? "" : "cancel"}
        escapeKeyAction={disabled ? "" : "cancel"}
    >
        <Header>
            <Title id="title" style="font-weight: 600;">Configure Weekly Target</Title>
        </Header>
        <Content id="content">
            <div class="form">
                <div class="input-container">
                    <Textfield
                        {disabled}
                        bind:value={target}
                        type="number"
                        input$name="target"
                        label="Weekly Target"
                        variant="outlined"
                        class="full-width"
                        required
                        input$min={0}
                        input$step={0.01}
                        input$inputmode="decimal"
                    >
                        <Icon class="material-symbols-rounded" slot="leadingIcon">payments</Icon>
                        <HelperText persistent slot="helper">0 means No Target</HelperText>
                    </Textfield>
                </div>
            </div>
        </Content>
        <Actions>
            <Button {disabled} type="button">
                <Label>Cancel</Label>
            </Button>

            <Button {disabled} on:click$stopPropagation defaultAction>
                <Label>Confirm</Label>
            </Button>
        </Actions>
    </Dialog>
</form>

<style>
    div.form {
        padding-top: 1em;
        align-items: center;
        align-content: center;
        width: 100%;
    }
</style>
