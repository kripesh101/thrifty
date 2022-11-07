<script>
    import LayoutGrid, { Cell } from "@smui/layout-grid";
    import TopAppBar, { Row, Section, Title, AutoAdjust } from "@smui/top-app-bar";
    import IconButton from "@smui/icon-button";
    import { state } from "@/stores";
    import fetchBackend from "@/lib/backend";
    import Button, { Label, Icon } from "@smui/button";
    import Expense from "@/lib/Expense.svelte";
    import Paper from "@smui/paper";
    import ExpensesDialog from "./ExpensesDialog.svelte";
    import { getContext, onMount, setContext } from "svelte";
    import { getThisWeek, getToday } from "@/lib/date";
    import CategoryChart from "@/lib/charts/CategoryChart.svelte";

    const snackbar = getContext("snackbar");

    let topAppBar;
    let chart;

    async function logout() {
        const res = await fetchBackend("/logout/", "post");
        if ((await res.json()) === true) {
            $state = "loggedout";
            snackbar("Logged out.", "success");
        }
    }

    let expensesDialogMode = false;
    let expensesDialogOpen = false;
    let expensesDialogData;

    function openExpensesDialog(data, editMode = false) {
        expensesDialogMode = editMode;
        expensesDialogData = data;
        expensesDialogOpen = true;
    }

    let weekTotal;
    let todayTotal;
    let expenses;
    function refresh(visible = true, callback) {
        if (visible) {
            weekTotal = "XXXX";
            todayTotal = "XXXX";
            expenses = "loading";
        }

        function expensesFetch(path = "") {
            return fetchBackend("/expenses/" + path);
        }

        function fetchTotal(obj) {
            return expensesFetch(`total/?timestamp_start=${obj.start}&timestamp_end=${obj.end}`);
        }

        Promise.all([
            fetchTotal(getThisWeek()),
            fetchTotal(getToday()),
            expensesFetch(),
            chart.reloadChart()
        ]).then(async (res) => {
            weekTotal = await res[0].json();
            todayTotal = await res[1].json();
            expenses = await res[2].json();
            callback();
        });
    }

    setContext("refresh", refresh);
    setContext("openExpensesDialog", openExpensesDialog);

    onMount(refresh);
</script>

<ExpensesDialog
    bind:data={expensesDialogData}
    bind:open={expensesDialogOpen}
    bind:editMode={expensesDialogMode}
/>

<TopAppBar bind:this={topAppBar} variant="fixed" dense>
    <Row>
        <Section>
            <Title>THRIFTY</Title>
        </Section>
        <Section align="end" toolbar>
            <IconButton on:click={logout} class="material-symbols-rounded">logout</IconButton>
        </Section>
    </Row>
</TopAppBar>

<AutoAdjust {topAppBar}>
    <LayoutGrid class="width: 100vw;">
        <Cell spanDevices={{ desktop: 12, tablet: 8, phone: 4 }}>
            <div class="mainInfo">
                <div class="text">
                    <h6>
                        THIS WEEK<br />
                        Rs. {weekTotal}
                    </h6>
                </div>
                <div class="circle">
                    <img src="https://picsum.photos/id/1037/200" alt="todo" />
                </div>
                <div class="text">
                    <h6>
                        TODAY<br />Rs. {todayTotal}
                    </h6>
                </div>
            </div>
        </Cell>
        <Cell spanDevices={{ desktop: 6, tablet: 8 }}>
            <CategoryChart bind:this={chart} />
        </Cell>
        <Cell spanDevices={{ desktop: 6, tablet: 8 }}>
            <div style="padding: 1em;">
                <Button
                    variant="raised"
                    style="padding: 20px;"
                    on:click={() => openExpensesDialog()}
                >
                    <Icon class="material-symbols-rounded">add</Icon>
                    <Label>ADD EXPENSES</Label>
                </Button>
            </div>
            <Paper>
                <h6 style="line-height: 1.6; text-align: left; margin: auto; font-weight: 600;">
                    History
                </h6>
                {#if expenses instanceof Array}
                    <!-- Loaded content from server -->
                    {#each expenses as data}
                        <Expense {data} />
                    {:else}
                        <i>No entries.</i>
                    {/each}
                {:else}
                    Loading...
                {/if}
            </Paper>
        </Cell>
    </LayoutGrid>
</AutoAdjust>

<style>
    .mainInfo {
        background-color: var(--mdc-theme-surface);
        border-radius: 20px;
        width: 100%;
        height: min(5em, 15vmin);
        box-shadow: 0px 0px 17px -5px rgba(0, 0, 0, 0.75);
        margin: auto;
        margin-top: 2em;
        margin-bottom: 2em;
        display: flex;
        align-items: center;
        justify-content: space-evenly;
        max-width: 800px;
    }

    .circle {
        position: relative;
        width: min(7em, 21vmin);
        height: min(7em, 21vmin);
        background: var(--mdc-theme-surface);
        border-radius: 50%;

        box-shadow: 0px 0px 17px -5px rgba(0, 0, 0, 0.65);
    }

    .circle:before {
        position: absolute;
        content: "";
        width: 15em;
        height: min(5em, 15vmin);
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: var(--mdc-theme-surface);
    }

    .circle img {
        position: absolute;
        max-width: 85%;
        border-radius: 50%;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 3;
    }

    img {
        width: 100%;
    }

    div.text {
        flex: 1;
        align-self: center;
        z-index: 2;
    }

    div.text h6 {
        font-weight: 600;
        font-size: min(1.25rem, 3.5vmin);
        line-height: 1.6;
    }
</style>
