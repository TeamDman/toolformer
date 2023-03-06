<script lang="ts">
	import Hello from "./hello.svelte";

	export let ratio: number;
</script>

<div class="split">
	<div class="left" style="width:calc(100% * {ratio})">
		<slot name="left">Left content not found.</slot>
	</div>
	<div class="right" style="width:calc(100% * (1-${ratio}))">
		<slot name="right">Right content not found.</slot>
	</div>
</div>

<style>
	.split {
		height: 100%;
		display: flex;
		flex-direction: row;
	}
</style>
