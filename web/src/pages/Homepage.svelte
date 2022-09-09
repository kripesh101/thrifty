<script>
    import LayoutGrid, { Cell } from "@smui/layout-grid";
    import TopAppBar, { Row, Section, Title, AutoAdjust } from "@smui/top-app-bar";
    import IconButton from "@smui/icon-button";
    import { state } from "../stores";
    import backend from "../lib/backend";
    import Button, { Label, Icon } from "@smui/button";
    import Expense from "../lib/Expense.svelte";
    import Paper from "@smui/paper";
    import record from "../lib/expenses.json";

    let expenses;
    expenses = record;

    let topAppBar;

    async function logout() {
        const res = await fetch(backend + "/logout/", {
            method: "POST",
            credentials: "include",
            mode: "cors"
        });
        if ((await res.json()) === true) {
            $state = "loggedout";
        }
    }
</script>

<TopAppBar bind:this={topAppBar} variant="standard" dense>
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
                        THIS WEEK<br />Rs. 7500
                    </h6>
                </div>
                <div class="circle">
                    <img src="https://picsum.photos/id/1037/200" alt="todo" />
                </div>
                <div class="text">
                    <h6>
                        TODAY<br />Rs. 1500
                    </h6>
                </div>
            </div>
        </Cell>
        <Cell spanDevices={{ desktop: 6, tablet: 4 }}>
            <!-- Graph will be here -->
            <img
                src="https://images.squarespace-cdn.com/content/v1/55b6a6dce4b089e11621d3ed/1585087896250-R3GZ6OFWYQRZUJRCJU3D/produce_monthly.png?format=1000w"
                alt="graph"
            />
        </Cell>
        <Cell spanDevices={{ desktop: 6, tablet: 4 }}>
            <div style="padding: 1em;">
                <Button variant="raised" style="padding: 20px;">
                    <Icon class="material-symbols-rounded">add</Icon>
                    <Label>ADD EXPENSES</Label>
                </Button>
            </div>
            <Paper>
                <h6 style="line-height: 1.6; text-align: left; margin: auto; font-weight: 600;">
                    History
                </h6>
                <Expense />
                {#each expenses as data}
                    <Expense {data} />
                {/each}
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
