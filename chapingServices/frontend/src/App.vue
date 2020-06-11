<template>
  <div id="app">
    <Home/>
  </div>
</template>

<script>
// import Home from './views/Home.vue'

export default {
  name: 'app',
  components: {
    // Home
    'Home': ()=>import('@/views/Home.vue')
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
}
body {

  }
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #c2ceda;
  /* margin-top: 60px; */
}
</style>
