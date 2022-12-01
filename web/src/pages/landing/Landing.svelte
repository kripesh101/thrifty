<script>
    import { push } from "svelte-spa-router";
    import Logo from "@/lib/Logo.svelte";
    import Button, { Label } from "@smui/button";
    import darkScreenshot from "./phone-screenshot-dark.png";
    import lightScreenshot from "./phone-screenshot-light.png";
    import LayoutGrid, { Cell } from "@smui/layout-grid";
</script>

<main>
    <LayoutGrid class="width: 100vw;">
        <Cell spanDevices={{ desktop: 6, tablet: 4, phone: 4 }}>
            <div class="title">
                <Logo />
                <h1>THRIFTY</h1>
            </div>
            <p>TRACK IT. SAVE IT.</p>

            <Button variant="raised" style="padding: 25px;" on:click={() => push("/start")}>
                <Label>Get Started!</Label>
            </Button>
        </Cell>
        <Cell spanDevices={{ desktop: 6, tablet: 4, phone: 4 }}>
            <div class="image-container">
                <picture>
                    <source srcset={darkScreenshot} media="(prefers-color-scheme:dark)" />
                    <img src={lightScreenshot} alt="Screenshot of Thrifty" />
                </picture>
            </div>
        </Cell>
    </LayoutGrid>
</main>

<style>
    main {
        text-align: left;
        padding: 1em;
    }

    h1 {
        line-height: 0.25em;
        font-family: "Azonix";
        font-size: 4rem;
    }

    p {
        font-size: 1.5em;
        line-height: 1.5em;
    }

    .image-container {
        padding: 1em;
        text-align: center;
    }

    img {
        height: 600px;
        box-shadow: 2px 2px 20px -5px;
        border-radius: 10px;
    }

    @media (prefers-color-scheme: dark) {
        img {
            color: #666;
        }
    }
</style>
