<script>
    import Button, { Label, Icon } from "@smui/button";

    let count = 0;
    const increment = () => {
        count += 1;
    };
</script>

<Button on:click={increment} variant="raised" style="transform: scale(1.5);">
    <Icon class="material-symbols-rounded">add</Icon>
    <Label>Add Expenses : {count}</Label>
</Button>
