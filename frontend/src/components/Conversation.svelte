<script lang="ts">
	import type { Props } from "../app";
	import List from "./List.svelte";
	import Message from "./Message.svelte";
	export let messages: Props<Message>[];

	$: listItems = messages.map((item) => {
		return {
			component: Message,
			props: {
				side: item.side,
				content: item.content,
				timestamp: item.timestamp,
				senderName: item.senderName,
			} as Props<Message>,
		};
	});

	let y = 0;
	$: {
		console.log(messages.length);
		y = 100;
	}
	// $: console.log(messages);
</script>

<svelte:window bind:scrollY={y} />

<List items={listItems} />
