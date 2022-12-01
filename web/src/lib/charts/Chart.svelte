<script>
    import { Chart } from "chart.js";
    import { onDestroy, setContext } from "svelte";
    import { fade } from "svelte/transition";
    import IconButton from "@smui/icon-button";
    import CircularProgress from "@smui/circular-progress";

    import { type, loading } from "./stores.js";
    import ChartSettings from "./ChartSettings.svelte";

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

        nextChart = optionsDialog.getNextChart();
        chart = await nextChart.update(canvas);
        title = nextChart.getTitle();

        processing = false;
    }
    setContext("reloadChart", reloadChart);

    onDestroy(() => {
        chart.destroy?.();
    });

    let optionsDialog;
    let dialogOpen = false;
</script>

<ChartSettings bind:this={optionsDialog} bind:open={dialogOpen} />

<div class="chart-header">
    <span class="chart-title">
        {title}
    </span>
    <IconButton class="material-symbols-rounded" on:click={() => (dialogOpen = true)}
        >tune</IconButton
    >
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
