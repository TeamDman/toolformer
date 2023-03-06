<script lang="ts">
	import type { ComponentType, SvelteComponentTyped } from "svelte";
	interface $$Props {
		left: ComponentType;
		right: ComponentType;
		leftParams: object;
		rightParams: object;
		ratio: number;
	}
	// type SL = $$Generic<object>;
	// type SR = $$Generic<object>;
	// type CL = $$Generic<object>;
	// type CR = $$Generic<object>;
	// type PL = $$Generic<object>;
	// type PR = $$Generic<object>;
	// // type TL = $$Generic<SvelteComponentTyped<SL,CL,PL>>;
	// // type TR = $$Generic<SvelteComponentTyped<SR,CR,PR>>;

	export let left: ConstructorOfATypedSvelteComponent;
	export let right: ConstructorOfATypedSvelteComponent;
	export let leftParams: object;
	export let rightParams: object;
	export let ratio: number = 0.5;
</script>

<div class="split">
	<div class="left" style="width:calc(100% * {ratio})">
		<svelte:component this={left} {...leftParams} />
	</div>
	<div class="right" style="width:calc(100% * (1-${ratio}))">
		<svelte:component this={right} {...rightParams} />
	</div>
</div>

<style>
	.split {
		height: 100%;
		display: flex;
		flex-direction: row;
	}
</style>
