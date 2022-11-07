<script>
    import { Icon } from "@smui/common";
    import Ripple from "@smui/ripple";
    import { getContext } from "svelte";
    import categories from "@/data/categories.json";

    export let data = {
        category: "restaurant",
        title: "Thakali",
        timestamp: 1656495900000,
        cost: 350
    };
    let parsedTime = "";

    const openExpensesDialog = getContext("openExpensesDialog");

    $: if (typeof data.timestamp === "number") {
        const date = new Date(data.timestamp);
        parsedTime =
            date.toLocaleDateString("en-US", {
                month: "long",
                year: "numeric",
                day: "numeric"
            }) +
            " - " +
            date
                .toLocaleTimeString("en-US", {
                    hour: "numeric",
                    minute: "numeric"
                })
                .replace(" ", "\xa0"); // Replace space with &nbsp;
    }
</script>

<div
    use:Ripple={{ surface: true }}
    on:click={() => openExpensesDialog(data, true)}
    tabindex="0"
    class="container"
>
    <div class="icon" style="background-color: {categories[data.category].color}">
        <Icon style="font-size: min(2.5em, 8vmin); color: white;" class="material-symbols-rounded"
            >{categories[data.category].icon}</Icon
        >
    </div>
    <div class="info">
        <span class="title">{data.title}</span><br />
        <span class="time">{parsedTime}</span>
    </div>
    <div class="cost-item">
        <span class="cost">Rs. {data.cost}</span>
    </div>
</div>

<style>
    .container {
        display: flex;
        justify-content: space-between;
        margin-top: 1em;
        margin-bottom: 1em;
        padding: 16px;
        border-radius: 4px;
        gap: 16px;
        backdrop-filter: brightness(1.35);
        -webkit-backdrop-filter: brightness(1.35);
        background-color: transparent;
    }

    .container div {
        align-self: center;
    }

    .title {
        font-weight: 600;
    }

    .icon {
        border-radius: 50px;
        width: min(4em, 12vmin);
        height: min(4em, 12vmin);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .info {
        flex: 1;
        text-align: left;
    }

    .info span {
        font-size: min(1.1em, 3.5vmin);
    }

    span.cost {
        font-size: min(1.2em, 3.8vmin);
    }

    @media (prefers-color-scheme: light) {
        .container {
            backdrop-filter: brightness(0.9);
            -webkit-backdrop-filter: brightness(0.9);
        }
    }
</style>
