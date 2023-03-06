<script lang="ts">
	import VerticalSplit from "../components/VerticalSplit.svelte";
	import Hello from "../components/hello.svelte";

	const activeComponent = VerticalSplit;
	let activeParameters = {
		left: Hello,
		right: Hello,
		leftParams: { backgroundColor: "blue" },
		rightParams: { backgroundColor: "red" },
		ratio: 0.2,
	};
</script>

<svelte:component this={activeComponent} {...activeParameters} />

<!-- <style>
	*,
	*::before,
	*::after {
		margin: 0;
		padding: 0;
		box-sizing: border-box;
	}
</style> -->
