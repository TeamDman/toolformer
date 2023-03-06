<script lang="ts">
	import { browser } from "$app/environment";
	import type { Props } from "../app";
	import ChatInput from "./ChatInput.svelte";
	import Conversation from "./Conversation.svelte";
	import Hello from "./hello.svelte";
	import HorizontalSplit from "./HorizontalSplit.svelte";
	import type Message from "./Message.svelte";
	import VerticalSplit from "./VerticalSplit.svelte";

	let messages: Props<Message>[] = [];

	let socket: WebSocket;
	if (browser) {
		socket = new WebSocket("ws://localhost:8765/");
		socket.addEventListener("open", () => {
			console.log("Connected");
			// socket.send("Hello, server!");
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
		});

		socket.addEventListener("message", (e) => {
			console.log(`Default view got ${e}`);
		});
	}

	async function onUserChatSubmit(e: CustomEvent<Props<Message>>) {
		console.log(e.detail);
		const message = e.detail as Props<Message>;
		socket.send(
			JSON.stringify({
				event: "message",
				message,
			}),
		);
		// messages.push(e.detail as Props<Message>);
		// messages = messages;
	}
</script>

<VerticalSplit ratio={0.2}>
	<div slot="left">
		<HorizontalSplit ratio={undefined}>
			<div slot="top">
				<Conversation {messages} />
			</div>
			<div slot="bottom" class="mt-2">
				<ChatInput on:submit={onUserChatSubmit} />
			</div>
		</HorizontalSplit>
	</div>
	<div slot="right">
		<Hello backgroundColor="blue" />
	</div>
</VerticalSplit>
