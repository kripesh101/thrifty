<script>
    import LayoutGrid, { Cell } from "@smui/layout-grid";
    import fetchBackend from "@/lib/backend";
    import { Icon } from "@smui/common";
    import Button, { Label } from "@smui/button";
    import Tooltip, { Wrapper } from "@smui/tooltip";
    import Expense from "@/lib/Expense.svelte";
    import Paper from "@smui/paper";
    import { getContext, onMount } from "svelte";
    import { getThisWeek, getToday } from "@/lib/date";
    import { push } from "svelte-spa-router";
    import { refreshImpl } from "./stores.js";
    import Chart from "@/lib/charts/Chart.svelte";

    const openExpensesDialog = getContext("openExpensesDialog");

    let chart;

    let weekTotal;
    let todayTotal;
    let expenses;
    let weeklyTarget;

    export async function refresh(visible = true) {
        if (visible) {
            weekTotal = "XXXX";
            todayTotal = "XXXX";
            expenses = "loading";
            weeklyTarget = null;
        }

        function expensesFetch(path = "") {
            return fetchBackend("/expenses/" + path);
        }

        function fetchTotal(obj) {
            return expensesFetch("total/" + params(obj));
        }

        function params(obj) {
            return `?timestamp_start=${obj.start}&timestamp_end=${obj.end}`;
        }

        const ret = new Promise((resolve, reject) => {
            Promise.all([
                fetchTotal(getThisWeek()),
                fetchTotal(getToday()),
                expensesFetch(params(getToday())),
                fetchBackend("/settings/weekly_target/"),
                chart.reloadChart()
            ])
                .then(async (res) => {
                    weekTotal = await res[0].json();
                    todayTotal = await res[1].json();
                    expenses = await res[2].json();
                    weeklyTarget = await res[3].json();
                    resolve();
                })
                .catch(reject);
        });

        return ret;
    }

    // eslint-disable-next-line prefer-const
    $refreshImpl = refresh;
    onMount(refresh);
</script>

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
                <Wrapper>
                    <div>
                        <Icon style="font-size: 3em" class="material-symbols-rounded">
                            {#if !weeklyTarget}
                                pending
                            {:else if weeklyTarget < weekTotal}
                                error
                            {:else}
                                check
                            {/if}
                        </Icon>
                    </div>
                    <Tooltip>
                        <b>Weekly Target: </b>
                        {#if weeklyTarget === 0}
                            Not Set
                        {:else if !weeklyTarget}
                            Loading...
                        {:else}
                            Rs. {weeklyTarget}
                        {/if}
                    </Tooltip>
                </Wrapper>
            </div>
            <div class="text">
                <h6>
                    TODAY<br />Rs. {todayTotal}
                </h6>
            </div>
        </div>
    </Cell>
    <Cell spanDevices={{ desktop: 6, tablet: 8 }}>
        <Chart bind:this={chart} />
    </Cell>
    <Cell spanDevices={{ desktop: 6, tablet: 8 }}>
        <div style="padding: 1em;">
            <Button variant="raised" style="padding: 20px;" on:click={() => openExpensesDialog()}>
                <Icon class="material-symbols-rounded">add</Icon>
                <Label>ADD EXPENSES</Label>
            </Button>
        </div>
        <Paper>
            <h6 style="line-height: 1.6; text-align: left; margin: auto; font-weight: 600;">
                Today's Expenses
            </h6>
            {#if expenses instanceof Array}
                <!-- Loaded content from server -->
                {#each expenses as data}
                    <Expense {data} />
                {:else}
                    <p><i>No entries today.</i></p>
                {/each}
            {:else}
                <p>Loading...</p>
            {/if}
            <div style="text-align: right; padding-top: 10px;">
                <Button on:click={() => push("/history")}>
                    <Label>View All</Label>
                    <Icon class="material-symbols-rounded">arrow_right_alt</Icon>
                </Button>
            </div>
        </Paper>
    </Cell>
</LayoutGrid>

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

    .circle div {
        position: absolute;
        border-radius: 50%;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 3;
        line-height: 0;
        padding: max(10px, 2.25vmin);
        backdrop-filter: brightness(2);
        -webkit-backdrop-filter: brightness(2);
        background-color: transparent;
    }

    @media (prefers-color-scheme: light) {
        .circle div {
            backdrop-filter: brightness(0.8);
            -webkit-backdrop-filter: brightness(0.8);
        }
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
