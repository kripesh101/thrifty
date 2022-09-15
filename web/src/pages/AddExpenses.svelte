<script>
    import Dialog, { Header, Title, Content, Actions } from "@smui/dialog";
    import Select, { Option } from "@smui/select";
    import IconButton from "@smui/icon-button";
    import Button, { Label } from "@smui/button";
    import Textfield from "@smui/textfield";
    import Icon from "@smui/textfield/icon";
    import DatePicker from "../lib/DatePicker.svelte";

    import { getContext } from "svelte";
    import categories from "../data/categories.json";
    import { postForm } from "../lib/backend";

    let disabled = false;
    export let data = {
        category: "",
        title: "",
        timestamp: 0,
        cost: "",
        description: ""
    };
    export let open;

    let currentData;
    let titleEdited;

    function copyData() {
        currentData = structuredClone(data);
        titleEdited = false;
    }
    copyData();

    const snackbar = getContext("snackbar");
    const refresh = getContext("refresh");
    async function handleFormSubmit(event) {
        disabled = true;

        const response = await postForm(event);

        if (response.ok) {
            if ((await response.json()) === true) {
                snackbar("Created new expense entry.", "success");
                refresh();
                disabled = false;
                open = false;
                return;
            }
        }

        snackbar("Error creating entry. Please try again.");

        disabled = false;
    }
</script>

<form action="/expenses/create/" on:submit|preventDefault={handleFormSubmit}>
    <Dialog
        bind:open
        fullscreen
        aria-labelledby="title"
        aria-describedby="content"
        on:SMUIDialog:opening={copyData}
        scrimClickAction={disabled ? "" : "cancel"}
        escapeKeyAction={disabled ? "" : "cancel"}
    >
        <Header>
            <Title id="title" style="align-self: stretch; font-weight: 600;">New Expense</Title>
            <IconButton
                {disabled}
                action="close"
                class="material-symbols-rounded"
                style="top: 10px;"
                type="button"
            >
                close
            </IconButton>
        </Header>
        <Content id="content">
            <div class="form">
                {#if open}
                    <div class="input-container">
                        <Textfield
                            {disabled}
                            bind:value={currentData.cost}
                            type="number"
                            input$name="cost"
                            label="Cost"
                            variant="outlined"
                            class="full-width"
                            required
                            input$min={0.01}
                            input$step={0.01}
                        >
                            <Icon class="material-symbols-rounded" slot="leadingIcon">payments</Icon
                            >
                        </Textfield>
                    </div>
                    <div class="input-container">
                        <Textfield
                            {disabled}
                            bind:value={currentData.title}
                            input$name="title"
                            label="Title"
                            variant="outlined"
                            class="full-width"
                            required
                            on:change={() => {
                                titleEdited = true;
                            }}
                        />
                    </div>
                    <div class="input-container">
                        <Select
                            bind:value={currentData.category}
                            label="Category"
                            variant="outlined"
                            input$name="category"
                            class="full-width"
                            hiddenInput
                            required
                            {disabled}
                            on:SMUISelect:change={() => {
                                if (!titleEdited) {
                                    currentData.title = categories[currentData.category].title;
                                }
                            }}
                        >
                            {#each Object.keys(categories) as category}
                                <Option value={category}>{categories[category].title}</Option>
                            {/each}
                        </Select>
                    </div>
                    <div class="input-container">
                        <DatePicker
                            {disabled}
                            name="timestamp"
                            bind:dateTime={currentData.timestamp}
                        />
                    </div>
                    <div class="input-container">
                        <Textfield
                            {disabled}
                            textarea
                            bind:value={currentData.description}
                            input$name="description"
                            label="Description"
                            variant="outlined"
                            class="full-width"
                            input$rows={6}
                        />
                    </div>
                {/if}
            </div>
        </Content>
        <Actions>
            <Button {disabled} action="cancel" type="button">
                <Label>Cancel</Label>
            </Button>
            <Button {disabled} action="confirm" on:click$stopPropagation defaultAction>
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
    div.input-container {
        max-width: 350px;
        margin: 0 auto;
        padding: 10px;
    }
</style>
