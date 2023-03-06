<script lang="ts">
	import Hello from "./hello.svelte";

	export let ratio: number | undefined;
</script>

{#if ratio === undefined}
	<div class="split">
		<div class="top">
			<slot name="top">Top content not found.</slot>
		</div>
		<div class="bottom">
			<slot name="bottom">Bottom content not found.</slot>
		</div>
	</div>
{:else}
	<div class="split">
		<div class="top" style="height:calc(100% * {ratio})">
			<slot name="top">Top content not found.</slot>
		</div>
		<div class="bottom" style="height:calc(100% * (1-${ratio}))">
			<slot name="bottom">Bottom content not found.</slot>
		</div>
	</div>
{/if}

<style>
	.split {
		height: 100%;
		display: flex;
		flex-direction: column;
	}
</style>
