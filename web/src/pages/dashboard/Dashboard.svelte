<script>
    import { getContext, setContext } from "svelte";
    import TopAppBar, { Row, Section, Title, AutoAdjust } from "@smui/top-app-bar";
    import IconButton from "@smui/icon-button";

    import { state } from "@/stores.js";
    import Router, { pop, location, replace } from "svelte-spa-router";
    import ExpenseHistory from "./ExpenseHistory.svelte";
    import ExpensesDialog from "./ExpensesDialog.svelte";
    import Homepage from "./Homepage.svelte";
    import fetchBackend from "@/lib/backend.js";
    import { refreshImpl } from "./stores.js";

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

    function refresh(visible) {
        $refreshImpl(visible);
    }

    async function logout() {
        const res = await fetchBackend("/logout/", "post");
        if ((await res.json()) === true) {
            $state = "loggedout";
            replace("/");
            snackbar("Logged out.", "success");
        }
    }

    let topAppBar;

    const routes = {
        "/": Homepage,
        "/history": ExpenseHistory,
        "*": Homepage
    };
</script>

<ExpensesDialog
    bind:data={expensesDialogData}
    bind:open={expensesDialogOpen}
    bind:editMode={expensesDialogEditMode}
/>

<TopAppBar bind:this={topAppBar} variant="fixed" dense>
    <Row>
        <Section>
            {#if $location !== "/"}
                <IconButton
                    on:click={async () => {
                        await pop();

                        // Make sure clicking the button takes us back to the dashboard home page.
                        setTimeout(() => {
                            if ($location !== "/") replace("/");
                        }, 50);
                    }}
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
    <Router {routes} />
</AutoAdjust>
