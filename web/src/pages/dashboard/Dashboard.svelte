<script>
    import Menu from "@smui/menu";
    import IconButton from "@smui/icon-button";
    import { getContext, setContext } from "svelte";
    import List, { Item, Graphic, Separator, Text } from "@smui/list";
    import Router, { pop, location, replace } from "svelte-spa-router";
    import TopAppBar, { Row, Section, Title, AutoAdjust } from "@smui/top-app-bar";

    import { state } from "@/stores.js";
    import Homepage from "./Homepage.svelte";
    import { refreshImpl } from "./stores.js";
    import fetchBackend from "@/lib/backend.js";
    import ExpenseHistory from "./ExpenseHistory.svelte";
    import ExpensesDialog from "./ExpensesDialog.svelte";
    import TargetDialog from "./TargetDialog.svelte";

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
    let menu;

    const routes = {
        "/": Homepage,
        "/history": ExpenseHistory,
        "*": Homepage
    };

    let targetDialogOpen;
</script>

<ExpensesDialog
    bind:data={expensesDialogData}
    bind:open={expensesDialogOpen}
    bind:editMode={expensesDialogEditMode}
/>

<TargetDialog bind:open={targetDialogOpen} />

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
            <div>
                <IconButton on:click={() => menu.setOpen(true)} class="material-symbols-rounded">
                    more_vert
                </IconButton>
                <Menu bind:this={menu}>
                    <List>
                        <Item on:SMUI:action={() => (targetDialogOpen = true)}>
                            <Graphic class="material-symbols-rounded">payments</Graphic>
                            <Text>Configure Weekly Target</Text>
                        </Item>
                        <Separator />
                        <Item on:SMUI:action={logout}>
                            <Graphic class="material-symbols-rounded">logout</Graphic>
                            <Text>Logout</Text>
                        </Item>
                    </List>
                </Menu>
            </div>
        </Section>
    </Row>
</TopAppBar>

<AutoAdjust {topAppBar}>
    <Router {routes} />
</AutoAdjust>
