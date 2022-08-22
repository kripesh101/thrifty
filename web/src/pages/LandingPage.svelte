<script>
    import Paper from "@smui/paper";
    import Tab, { Label } from "@smui/tab";
    import TabBar from "@smui/tab-bar";

    import LoginForm from "./LoginForm.svelte";
    import RegisterForm from "./RegisterForm.svelte";

    let active = "Login";
</script>

<h2 style="line-height:0">THRIFTY</h2>

<Paper>
    <div>
        <TabBar tabs={["Login", "Register"]} let:tab bind:active>
            <Tab {tab}>
                <Label>{tab}</Label>
            </Tab>
        </TabBar>
    </div>

    <div>
        {#if active === "Login"}
            <LoginForm />
        {:else if active === "Register"}
            <RegisterForm />
        {/if}
    </div>
</Paper>

<style>
    div {
        padding: 10px;
        align-self: center;
    }
</style>
