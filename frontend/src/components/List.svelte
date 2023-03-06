<script lang="ts">
	export let items: {
		component: ConstructorOfATypedSvelteComponent;
		props: object;
	}[];
</script>

<div class="list">
	{#each items as item}
		<svelte:component this={item.component} {...item.props} />
	{/each}
</div>

<style>
	.list {
		display: flex;
		flex-direction: column;
	}
</style>
