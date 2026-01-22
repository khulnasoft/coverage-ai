<script>
	import Calculator from '$lib/components/Calculator.svelte';
</script>

<main>
	<h1>Svelte Calculator</h1>
	<Calculator />
</main>

<style>
	main {
		text-align: center;
		padding: 2em;
		max-width: 400px;
		margin: 0 auto;
	}
	
	h1 {
		color: #ff3e00;
		margin-bottom: 2em;
	}
</style>
