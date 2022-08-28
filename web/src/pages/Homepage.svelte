<script>
    import LayoutGrid, { Cell } from "@smui/layout-grid";
    import TopAppBar, { Row, Section, Title, AutoAdjust } from "@smui/top-app-bar";
    import IconButton from "@smui/icon-button";
    import { state } from "../stores";
    import backend from "../lib/backend";

    let topAppBar;

    async function logout() {
        const res = await fetch(backend + "/logout/", {
            method: "POST",
            credentials: "include",
            mode: "cors"
        });
        if ((await res.json()).success) {
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
        <Cell spanDevices={{ desktop: 6, tablet: 4 }}>test</Cell>
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
        z-index: 200;
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
