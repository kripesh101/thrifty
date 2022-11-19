<script>
    import { getContext, setContext } from "svelte";
    import TopAppBar, { Row, Section, Title, AutoAdjust } from "@smui/top-app-bar";
    import IconButton from "@smui/icon-button";

    import { dashboardState } from "./stores.js";
    import { state } from "@/stores.js";
    import ExpenseHistory from "./ExpenseHistory.svelte";
    import ExpensesDialog from "./ExpensesDialog.svelte";
    import Homepage from "./Homepage.svelte";
    import fetchBackend from "@/lib/backend.js";

    setContext("openExpensesDialog", openExpensesDialog);
    setContext("refresh", refresh);
    const snackbar = getContext("snackbar");

    let expensesDialogEditMode = false;
    let expensesDialogOpen = false;
    let expensesDialogData;

    function openExpensesDialog(data, editMode = false) {
        expensesDialogEditMode = editMode;
        expensesDialogData = data;
        expensesDialogOpen = true;
    }

    function refresh(visible, callback) {
        context.refresh(visible, callback);
    }

    async function logout() {
        const res = await fetchBackend("/logout/", "post");
        if ((await res.json()) === true) {
            $state = "landing";
            snackbar("Logged out.", "success");
        }
    }

    let context;
    $: currentPage = $dashboardState === "homepage" ? Homepage : ExpenseHistory;

    let topAppBar;
</script>

<ExpensesDialog
    bind:data={expensesDialogData}
    bind:open={expensesDialogOpen}
    bind:editMode={expensesDialogEditMode}
/>

<TopAppBar bind:this={topAppBar} variant="fixed" dense>
    <Row>
        <Section>
            {#if $dashboardState !== "homepage"}
                <IconButton
                    on:click={() => ($dashboardState = "homepage")}
                    class="material-symbols-rounded"
                >
                    arrow_back
                </IconButton>
            {/if}
            <Title>THRIFTY</Title>
        </Section>
        <Section align="end" toolbar>
            <IconButton on:click={logout} class="material-symbols-rounded">logout</IconButton>
        </Section>
    </Row>
</TopAppBar>

<AutoAdjust {topAppBar}>
    <svelte:component this={currentPage} bind:this={context} />
</AutoAdjust>
