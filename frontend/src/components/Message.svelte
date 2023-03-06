<script lang="ts">
	export let side: "left" | "right";
	export let content: string;
	export let timestamp: number;
	export let senderName: string;
	$: right = side === "right";
</script>

<div class="message rounded-md p-1 mt-1" class:bg-blue-400={right} class:self-end={right}>
	<div>
		<div class="message-sender font-bold">{senderName}</div>
		<div class="message-timestamp text-gray-500">{timestamp}</div>
	</div>
	<div class="message-body">{content}</div>
</div>

<style>
	.message:not(:hover) .message-timestamp {
		display: none;
	}
</style>
