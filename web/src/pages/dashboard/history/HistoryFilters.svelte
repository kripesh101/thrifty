<script>
    import Chip, { Set, Text } from "@smui/chips";
    import categories from "@/data/categories.json";
    import Button, { Label } from "@smui/button";
    import Checkbox from "@smui/checkbox";
    import FormField from "@smui/form-field";
    import DatePicker from "@/lib/DatePicker.svelte";
    import { getContext } from "svelte";

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
            }
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
            params += `timestamp_end=${filters.date.to.timestamp}&`;
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
    <div class="option-container date">
        <b>Range:</b>
        <br />
        <FormField>
            <Checkbox bind:checked={config.filters.date.from.enabled} />
            <span slot="label">From</span>
        </FormField>
        {#if config.filters.date.from.enabled}
            <DatePicker bind:dateTime={config.filters.date.from.timestamp} />
        {/if}
    </div>
    <div class="option-container date">
        <FormField>
            <Checkbox bind:checked={config.filters.date.to.enabled} />
            <span slot="label">To</span>
        </FormField>
        {#if config.filters.date.to.enabled}
            <DatePicker bind:dateTime={config.filters.date.to.timestamp} />
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
</style>
