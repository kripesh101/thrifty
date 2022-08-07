<script>
    import Button, { Label, Icon } from "@smui/button";

    let count = 0;
    const increment = () => {
        count += 1;
    };
</script>

<Button on:click={increment} variant="raised" style="padding: 28px;">
    <Icon style="transform: scale(1.5); padding-right: 10px;" class="material-symbols-rounded">
        add
    </Icon>
    <Label style="font-size: 20px;">Add Expenses : {count}</Label>
</Button>
