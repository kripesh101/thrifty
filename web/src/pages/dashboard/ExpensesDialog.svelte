<script>
    import Dialog, { Header, Title, Content, Actions } from "@smui/dialog";
    import Select, { Option } from "@smui/select";
    import IconButton from "@smui/icon-button";
    import Button, { Label } from "@smui/button";
    import Textfield from "@smui/textfield";
    import Icon from "@smui/textfield/icon";
    import { getContext } from "svelte";

    import DatePicker from "@/lib/DatePicker.svelte";
    import categories from "@/data/categories.json";
    import fetchBackend, { postForm } from "@/lib/backend";
    import { fakeFocusIOS } from "@/lib/hacks";

    const defaultData = {
        category: "",
        title: "",
        timestamp: null,
        cost: "",
        description: ""
    };

    export let data;
    export let open;
    export let editMode = false;

    let disabled = false;
    let currentData;
    let titleEdited;
    let focus;
    let confirmOpen;

    function copyData(event) {
        if (!data) data = defaultData;
        currentData = structuredClone(data);
        titleEdited = editMode
            ? currentData.title !== categories[currentData.category].title
            : false;
        if (event && !editMode) fakeFocusIOS();
    }
    copyData();

    const snackbar = getContext("snackbar");
    const refresh = getContext("refresh");

    async function handleFormSubmit(event) {
        // "Confirm" button clicked
        disabled = true;

        let response;
        if (editMode) {
            response = await postForm(event, "put", `/expenses/edit/${currentData.id}`);
        } else {
            response = await postForm(event);
        }

        if (response.ok && (await response.json()) === true) {
            if (editMode) {
                await refresh(false);
                snackbar("Edited expense entry.", "success");
                open = false;
                disabled = false;
                return;
            }

            snackbar("Created new expense entry.", "success");
            refresh();
            open = false;
        } else {
            snackbar(
                "Error submitting entry. Please ensure all required fields are filled out and try again."
            );
        }

        disabled = false;
    }

    async function deleteEntry() {
        disabled = true;

        const response = await fetchBackend(`/expenses/delete/${currentData.id}`, "delete");

        if (response.ok && (await response.json()) === true) {
            await refresh(false);
            snackbar("Deleted expense entry.", "success");
            open = false;
            disabled = false;
            return;
        } else {
            snackbar("Error deleting entry. Please try again.");
        }

        disabled = false;
    }

    function confirmClose(e) {
        if (e.detail.action === "accept") {
            deleteEntry();
        }
    }
</script>

<form action="/expenses/create/" on:submit|preventDefault={handleFormSubmit}>
    <Dialog
        bind:open
        fullscreen
        aria-labelledby="title"
        aria-describedby="content"
        on:SMUIDialog:opening={copyData}
        on:SMUIDialog:opened={() => {
            if (!editMode) focus();
        }}
        scrimClickAction={disabled ? "" : "cancel"}
        escapeKeyAction={disabled ? "" : "cancel"}
    >
        <Header>
            <Title id="title" style="align-self: stretch; font-weight: 600;">
                {#if editMode}
                    Edit Expense
                {:else}
                    New Expense
                {/if}
            </Title>
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
                        input$inputmode="decimal"
                        bind:focus
                    >
                        <Icon class="material-symbols-rounded" slot="leadingIcon">payments</Icon>
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
                {#if open}
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
                {/if}
                <div class="input-container">
                    <Textfield
                        {disabled}
                        bind:value={currentData.description}
                        textarea
                        input$name="description"
                        label="Description"
                        variant="outlined"
                        class="full-width"
                        input$rows={6}
                    />
                </div>
            </div>
        </Content>
        <Actions>
            <Button {disabled} type="button">
                <Label>Cancel</Label>
            </Button>

            {#if editMode}
                <Button
                    {disabled}
                    on:click$stopPropagation={() => {
                        confirmOpen = true;
                    }}
                    type="button"
                >
                    <Label>Delete</Label>
                </Button>
            {/if}

            <Button {disabled} on:click$stopPropagation defaultAction>
                <Label>
                    {#if editMode}
                        Edit
                    {:else}
                        Confirm
                    {/if}
                </Label>
            </Button>
        </Actions>

        <Dialog
            bind:open={confirmOpen}
            slot="over"
            on:SMUIDialog:closed={confirmClose}
            aria-labelledby="confirm-title"
            aria-describedby="confirm-content"
            style="text-align: left;"
        >
            <Header>
                <Title id="confirm-title" style="font-weight: 600;">Confirmation</Title>
            </Header>
            <Content id="confirm-content">
                <p>Are you sure you want to delete this expense entry?</p>
            </Content>
            <Actions>
                <Button type="button">
                    <Label>No</Label>
                </Button>
                <Button action="accept" type="button" defaultAction>
                    <Label>Yes</Label>
                </Button>
            </Actions>
        </Dialog>
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
