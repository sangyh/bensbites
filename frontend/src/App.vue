<template>
  <HelloWorld msg="Welcome to Your Vue.js App"/>
  <Home/>
</template>

<script>
import Home from './components/SearchHome.vue'

export default {
  name: 'App',
  components: {
    Home
  }
}
</script>

<style>
/* #app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
} */
</style>
