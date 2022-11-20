<script>
    import Logo from "@/lib/Logo.svelte";
    import Paper from "@smui/paper";
    import Tab, { Label } from "@smui/tab";
    import TabBar from "@smui/tab-bar";

    import LoginForm from "./LoginForm.svelte";
    import RegisterForm from "./RegisterForm.svelte";

    let active = "Login";
</script>

<main>
    <div class="container">
        <Logo />

        <h2>THRIFTY</h2>
        <Paper style="padding-top: 16px; padding-bottom: 16px;">
            <div class="form">
                <TabBar tabs={["Login", "Register"]} let:tab bind:active>
                    <Tab {tab}>
                        <Label>{tab}</Label>
                    </Tab>
                </TabBar>
            </div>

            <div class="form">
                {#if active === "Login"}
                    <LoginForm />
                {:else if active === "Register"}
                    <RegisterForm />
                {/if}
            </div>
        </Paper>
    </div>
</main>

<style>
    main {
        display: flex;
        place-items: center;
        min-width: 320px;
        min-height: 100vh;
    }

    .container {
        margin: 0 auto;
    }

    .form {
        padding: 10px;
        align-self: center;
    }
    h2 {
        margin: 0 0 10px 0;
        font-family: "Azonix";
        font-size: 4em;
    }
</style>
