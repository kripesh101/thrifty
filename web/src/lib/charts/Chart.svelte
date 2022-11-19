<script>
    import { Chart } from "chart.js";
    import { onDestroy, onMount } from "svelte";
    import { fade } from "svelte/transition";
    import IconButton from "@smui/icon-button";
    import CircularProgress from "@smui/circular-progress";
    import { type, loading } from "./stores.js";
    import SummaryChart from "./summary.js";
    import CategoryChart from "./category.js";

    Chart.defaults.font.family = "Montserrat";
    Chart.defaults.font.size = 14;

    let canvas;
    let chart;
    let title = "Loading...";

    let nextChart;

    let processing = false;
    export async function reloadChart() {
        if (processing) return;
        processing = true;

        chart = await nextChart.update(canvas);
        title = nextChart.getTitle();

        processing = false;
    }

    onDestroy(() => {
        chart.destroy?.();
    });

    onMount(() => {
        nextChart = $type === "category" ? CategoryChart : SummaryChart;
    });

    function swapChart() {
        if (processing) return;

        if (nextChart === SummaryChart) {
            if (SummaryChart.options.type === "week") SummaryChart.options.type = "year";
            else {
                CategoryChart.options.type = "month";
                nextChart = CategoryChart;
            }
        } else if (nextChart === CategoryChart) {
            if (CategoryChart.options.type === "month") CategoryChart.options.type = "overall";
            else if (CategoryChart.options.type === "overall") CategoryChart.options.type = "today";
            else if (CategoryChart.options.type === "today") CategoryChart.options.type = "week";
            else if (CategoryChart.options.type === "week") CategoryChart.options.type = "year";
            else {
                SummaryChart.options.type = "week";
                nextChart = SummaryChart;
            }
        }

        reloadChart();
    }
</script>

<div class="chart-header">
    <span class="chart-title">
        {title}
    </span>
    <IconButton class="material-symbols-rounded" on:click={swapChart}>tune</IconButton>
</div>
<div class="canvas-container" class:wide={$type === "summary"}>
    <canvas bind:this={canvas} />
    {#if $loading}
        <div class="overlay" out:fade>
            <div class="circular-progress" transition:fade>
                <CircularProgress style="height: 32px; width: 32px;" indeterminate />
            </div>
        </div>
    {/if}
</div>

<style>
    .chart-title {
        font-weight: 600;
        font-size: 1.2em;
    }

    .chart-header {
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 500px;
        padding-bottom: 5px;
    }

    .canvas-container {
        margin: 0 auto;
        max-height: 420px;
        aspect-ratio: 1;
        position: relative;
    }
    .canvas-container.wide {
        aspect-ratio: 2;
    }

    .overlay {
        z-index: 1;
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        background-color: #000;
    }
    .circular-progress {
        padding-top: 100px;
    }

    @media (prefers-color-scheme: light) {
        .overlay {
            background-color: #fff;
        }
    }
</style>
