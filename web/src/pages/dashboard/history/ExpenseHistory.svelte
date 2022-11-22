<script>
    import { onMount } from "svelte";
    import Expense from "@/lib/Expense.svelte";
    import fetchBackend from "@/lib/backend";
    import { refreshImpl } from "@/pages/dashboard/stores.js";
    import Accordion, { Panel, Header, Content } from "@smui-extra/accordion";
    import IconButton from "@smui/icon-button";
    import Button from "@smui/button";
    import { Label } from "@smui/common";
    import HistoryFilters from "./HistoryFilters.svelte";

    let expenses;
    let filter;
    let total;

    export async function refresh(visible = true) {
        const filterQuery = filter.getFilterParams();
        if (filterQuery === null) return;

        if (visible) {
            expenses = "loading";
            total = "XXXX";
        }

        const res = await Promise.all([
            fetchBackend("/expenses/" + filterQuery + filter.getSortParams()),
            fetchBackend("/expenses/total/" + filterQuery)
        ]);
        expenses = await res[0].json();
        total = await res[1].json();
    }

    // eslint-disable-next-line prefer-const
    $refreshImpl = refresh;
    onMount(refresh);
</script>

<Accordion multiple style="margin: 1em auto 1em; max-width: 800px;">
    <Panel>
        <Header>
            <h3>Sort & Filter</h3>
            <IconButton slot="icon" class="material-symbols-rounded">tune</IconButton>
        </Header>
        <Content>
            <form on:submit|preventDefault={() => refresh()}>
                <HistoryFilters bind:this={filter} />
                <div class="actions">
                    <Button
                        type="button"
                        on:click={() => {
                            filter.reset();
                            refresh();
                        }}
                    >
                        <Label>Reset</Label>
                    </Button>
                    <Button variant="raised" type="submit">
                        <Label>Apply</Label>
                    </Button>
                </div>
            </form>
        </Content>
    </Panel>

    <Panel nonInteractive open>
        <Content>
            <h3 class="total">Total Amount: <br />Rs. {total}</h3>
        </Content>
    </Panel>

    <Panel nonInteractive open>
        <Content>
            <h3>History</h3>
            {#if expenses instanceof Array}
                <!-- Loaded content from server -->
                {#each expenses as data}
                    <Expense {data} />
                {:else}
                    <p><i>No entries.</i></p>
                {/each}
            {:else}
                <p>Loading...</p>
            {/if}
        </Content>
    </Panel>
</Accordion>

<style>
    h3 {
        line-height: 1.6;
        text-align: left;
        margin: auto;
        font-weight: 600;
        font-size: 1.25rem;
    }

    form {
        text-align: left;
    }

    .actions {
        text-align: right;
    }

    .total {
        text-align: center;
    }
</style>
