<script>
    import Chip, { Set, Text } from "@smui/chips";
    import categories from "@/data/categories.json";
    import Button, { Label } from "@smui/button";
    import Checkbox from "@smui/checkbox";
    import FormField from "@smui/form-field";
    import DatePicker from "@/lib/DatePicker.svelte";
    import { getContext } from "svelte";
    import Textfield from "@smui/textfield";
    import Icon from "@smui/textfield/icon";
    import HelperText from "@smui/textfield/helper-text";

    const snackbar = getContext("snackbar");
    const configDefault = {
        filters: {
            categories: Object.keys(categories),
            date: {
                from: {
                    enabled: false,
                    timestamp: null
                },
                to: {
                    enabled: false,
                    timestamp: null
                }
            },
            textFilter: ""
        },
        sort: {
            by: "timestamp",
            order: "desc"
        }
    };
    let config;
    reset();

    const choices = {
        sort: {
            by: {
                cost: "Cost",
                timestamp: "Time"
            },
            order: {
                desc: "Descending",
                asc: "Ascending"
            }
        }
    };

    export function reset() {
        config = structuredClone(configDefault);
    }

    export function getFilterParams() {
        let params = "?";
        const filters = config.filters;

        if (!filters.categories.length) {
            snackbar("No categories selected! You must pick at least one category.");
            return null;
        }

        params += filters.categories.reduce((prev, val) => `${prev}category=${val}&`, "");

        if (filters.date.from.enabled) {
            params += `timestamp_start=${filters.date.from.timestamp}&`;
        }
        if (filters.date.to.enabled) {
            // Add 1 day so the selected date is also included
            const date = new Date(filters.date.to.timestamp);
            date.setDate(date.getDate() + 1);
            params += `timestamp_end=${date.getTime()}&`;
        }

        if (filters.textFilter) {
            params += `text_filter=${filters.textFilter}&`;
        }

        return params;
    }

    export function getSortParams() {
        const sort = config.sort;
        return `&sort_by=${sort.by}&order=${sort.order}`;
    }
</script>

<div class="type" style="margin-top: 0;">
    <h4>Filters</h4>
    <div class="option-container">
        <b>Title / Description:</b>
        <br />
        <div class="input-container">
            <Textfield
                bind:value={config.filters.textFilter}
                input$pattern={"[A-Za-z0-9\\s]{0,500}"}
                input$maxlength={500}
                input$title="Numbers, spaces and letters only. Maximum length: 500"
                label="Query"
                variant="outlined"
            >
                <Icon class="material-symbols-rounded" slot="leadingIcon">search</Icon>
                <HelperText validationMsg slot="helper">Invalid characters.</HelperText>
            </Textfield>
        </div>
    </div>
    <div class="option-container date">
        <b>Date Range:</b>
        <br />
        <FormField>
            <Checkbox bind:checked={config.filters.date.from.enabled} />
            <span slot="label">From</span>
        </FormField>
        {#if config.filters.date.from.enabled}
            <div class="input-container">
                <DatePicker
                    bind:dateTime={config.filters.date.from.timestamp}
                    fullWidth={false}
                    dateOnly={true}
                />
            </div>
        {/if}
    </div>
    <div class="option-container date">
        <FormField>
            <Checkbox bind:checked={config.filters.date.to.enabled} />
            <span slot="label">To</span>
        </FormField>
        {#if config.filters.date.to.enabled}
            <div class="input-container">
                <DatePicker
                    bind:dateTime={config.filters.date.to.timestamp}
                    fullWidth={false}
                    dateOnly={true}
                />
            </div>
        {/if}
    </div>
    <div class="option-container">
        <b>Categories:</b>
        <br />

        <Button color="secondary" type="button" on:click={() => (config.filters.categories = [])}>
            <Label>Unselect All</Label>
        </Button>
        <Button
            color="secondary"
            type="button"
            on:click={() => (config.filters.categories = Object.keys(categories))}
        >
            <Label>Select All</Label>
        </Button>
        <Set
            chips={Object.keys(categories)}
            let:chip
            filter
            bind:selected={config.filters.categories}
        >
            <Chip {chip}>
                <Text>{categories[chip].title}</Text>
            </Chip>
        </Set>
    </div>
</div>
<div class="type" style="margin-top: 0;">
    <h4>Sorting</h4>
    <div class="option-container">
        <b>Sort By:</b>
        <Set chips={Object.keys(choices.sort.by)} let:chip choice bind:selected={config.sort.by}>
            <Chip {chip}>
                <Text>{choices.sort.by[chip]}</Text>
            </Chip>
        </Set>
    </div>
    <div class="option-container">
        <b>Order By:</b>
        <Set
            chips={Object.keys(choices.sort.order)}
            let:chip
            choice
            bind:selected={config.sort.order}
        >
            <Chip {chip}>
                <Text>{choices.sort.order[chip]}</Text>
            </Chip>
        </Set>
    </div>
</div>

<style>
    h4 {
        font-size: 1.15rem;
        font-weight: 600;
        line-height: 1.6;
        margin: auto;
        margin-bottom: 0.6em;
    }

    .option-container {
        margin-left: 1.5em;
    }

    .type {
        margin: 1em 0;
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
