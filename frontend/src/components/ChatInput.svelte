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
			senderName: "User (web ui)",
		} as Props<Message>);
		input = "";
	}

	let input = "";
</script>

<form on:submit|preventDefault={submit} class="flex">
	<input
		type="text"
		bind:value={input}
		placeholder="Type a message..."
		class="p-1 rounded-md bg-black border-green-800 border-2 text-white"
	/>
	<button type="submit" class="ml-1">
		<i class="mi mi-send text-green-800"><span class="u-sr-only">Send</span></i>
	</button>
</form>
