<script lang="ts">
	import { createEventDispatcher } from "svelte";
	import type { Props } from "../app";
	import type Message from "./Message.svelte";
	const dispatch = createEventDispatcher();
	function submit(e: Event) {
		dispatch("submit", {
			side: "right",
			content: input,
			timestamp: new Date().getTime(),
			senderName: "John",
		} as Props<Message>);
	}

	let input = "";
</script>

<form on:submit|preventDefault={submit} class="flex">
	<input
		type="text"
		bind:value={input}
		placeholder="Type a message..."
		class="p-1 rounded-md shadow-lg border-gray-400 border-2"
	/>
	<button type="submit">
		<i class="mi mi-send text-blue-500"><span class="u-sr-only">Send</span></i>
	</button>
</form>
