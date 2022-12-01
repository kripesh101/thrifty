<script>
    import Dialog, { Actions, Content, Header, Title } from "@smui/dialog";
    import Button, { Label } from "@smui/button";
    import Radio from "@smui/radio";

    import { getContext } from "svelte";
    import FormField from "@smui/form-field";
    import DatePicker from "../DatePicker.svelte";
    import SummaryChart from "./summary.js";
    import CategoryChart from "./category.js";

    export let open;
    let disabled;

    const reloadChart = getContext("reloadChart");

    async function handleFormSubmit() {
        // "Confirm" button clicked
        disabled = true;

        selectedBackup = selected;

        // Apply changes
        const options = selected.split("-");

        if (options[0] === "summary") {
            // @ts-ignore
            SummaryChart.options.type = options[1];
            SummaryChart.options.timestamp = date;
        } else {
            // @ts-ignore
            CategoryChart.options.type = options[1];
        }

        await reloadChart();

        disabled = false;
        open = false;
    }

    export function getNextChart() {
        return selected.startsWith("summary") ? SummaryChart : CategoryChart;
    }

    let selected = "summary-week";
    let selectedBackup;
    let date;
</script>

<form on:submit|preventDefault={handleFormSubmit}>
    <Dialog
        bind:open
        aria-labelledby="title"
        aria-describedby="content"
        on:SMUIDialog:opening={() => {
            selectedBackup = selected;
            date = SummaryChart.options.timestamp;
        }}
        on:SMUIDialog:closed={() => (selected = selectedBackup)}
        scrimClickAction={disabled ? "" : "cancel"}
        escapeKeyAction={disabled ? "" : "cancel"}
    >
        <Header>
            <Title id="title" style="font-weight: 600;">Configure Chart</Title>
        </Header>
        <Content id="content">
            <div class="type" style="margin-top: 0;">
                <h4>Category Chart</h4>
                <div class="option-container date">
                    <FormField>
                        <Radio bind:group={selected} value="category-today" {disabled} />
                        <span slot="label">Today</span>
                    </FormField>
                    <FormField>
                        <Radio bind:group={selected} value="category-week" {disabled} />
                        <span slot="label">This Week</span>
                    </FormField>
                    <FormField>
                        <Radio bind:group={selected} value="category-month" {disabled} />
                        <span slot="label">This Month</span>
                    </FormField>
                    <FormField>
                        <Radio bind:group={selected} value="category-year" {disabled} />
                        <span slot="label">This Year</span>
                    </FormField>
                    <FormField>
                        <Radio bind:group={selected} value="category-overall" {disabled} />
                        <span slot="label">Overall</span>
                    </FormField>
                </div>
                <div class="type" style="margin-top: 0;">
                    <h4>Summary Chart</h4>
                    <div class="option-container date">
                        <FormField>
                            <Radio bind:group={selected} value="summary-week" {disabled} />
                            <span slot="label">Weekly</span>
                        </FormField>
                        <FormField>
                            <Radio bind:group={selected} value="summary-year" {disabled} />
                            <span slot="label">Yearly</span>
                        </FormField>
                        {#if selected.startsWith("summary")}
                            <p>
                                Pick any day in the desired {selected.includes("week")
                                    ? "week"
                                    : "year"}:
                            </p>
                            <div class="input-container">
                                {#if open}
                                    <DatePicker
                                        bind:dateTime={date}
                                        fullWidth={false}
                                        dateOnly={true}
                                    />
                                {/if}
                            </div>
                        {/if}
                    </div>
                </div>
            </div></Content
        >
        <Actions>
            <Button {disabled} type="button">
                <Label>Cancel</Label>
            </Button>

            <Button {disabled} on:click$stopPropagation defaultAction>
                <Label>Confirm</Label>
            </Button>
        </Actions>
    </Dialog>
</form>

<style>
    h4 {
        font-size: 1.15rem;
        font-weight: 600;
        line-height: 1.6;
        margin: auto;
        margin-bottom: 0.6em;
    }

    .type {
        margin: 1em 0;
        text-align: left;
    }

    .date {
        max-width: 450px;
        margin-bottom: 1em;
    }

    .input-container {
        padding-top: 0.5em;
        padding-left: 0.5em;
    }
</style>
