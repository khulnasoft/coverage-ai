<template>
  <div id="app">
    <h1>Vue Calculator</h1>
    <Calculator />
  </div>
</template>

<script>
import Calculator from './components/Calculator.vue'

export default {
  name: 'App',
  components: {
    Calculator
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

h1 {
  color: #42b883;
  margin-bottom: 2rem;
}
</style>
