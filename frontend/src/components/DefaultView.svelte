<script lang="ts">
	import { browser } from "$app/environment";
	import { onDestroy } from "svelte";
	import type { Props } from "../app";
	import ChatInput from "./ChatInput.svelte";
	import Conversation from "./Conversation.svelte";
	import Hello from "./hello.svelte";
	import HorizontalSplit from "./HorizontalSplit.svelte";
	import type Message from "./Message.svelte";
	import Shader from "./Shader.svelte";
	import VerticalSplit from "./VerticalSplit.svelte";

	let messages: Props<Message>[] = [];

	let socket: WebSocket | null = null;
	let connected = false;
	let dots = "...";
	function connect() {
		socket = new WebSocket("ws://localhost:8765/");
		socket.addEventListener("open", () => {
			console.log("Connected");
			connected = true;
		});

		socket.addEventListener("message", (event) => {
			console.log(`Server says: ${event.data}`);
			try {
				const data = JSON.parse(event.data);
				console.log(data);
				if (data.event === "message") {
					const message = data.message as Props<Message>;
					console.log("was a message", message);
					messages.push(message);
					messages = messages;
				} else if (data.event === "history") {
					const history = data.history as Props<Message>[];
					console.log("was a history", history);
					messages = history;
				}
			} catch (e) {
				console.log("Not JSON");
			}
		});

		socket.addEventListener("close", () => {
			console.log("Disconnected");
			connected = false;
			socket = null;
		});
		return socket;
	}

	if (browser) {
		socket = connect();
	}

	const dotsInterval = setInterval(() => {
		if (!connected) {
			dots += ".";
			if (dots.length > 3) {
				dots = "";
			}
			if (socket == null) {
				socket = connect();
			}
		}
	}, 500);
	onDestroy(() => {
		clearInterval(dotsInterval);
	});

	async function onUserChatSubmit(e: CustomEvent<Props<Message>>) {
		console.log(e.detail);
		const message = e.detail as Props<Message>;
		if (socket != null) {
			socket.send(
				JSON.stringify({
					event: "message",
					message,
				}),
			);
		}
	}
</script>

{#if connected}
	<div class="m-2">
		<HorizontalSplit ratio={undefined}>
			<div slot="top">
				<Conversation {messages} />
			</div>
			<div slot="bottom" class="mt-2">
				<ChatInput on:submit={onUserChatSubmit} />
			</div>
		</HorizontalSplit>
	</div>
{:else}
	<Shader />
	<div class="absolute top-0 left-0 w-full h-full flex justify-center items-center">
		<div class="text-2xl text-white">Waiting for server{dots}</div>
	</div>
{/if}
