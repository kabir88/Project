<template>
  <div id="app">
    <header>
      <h1>NBA Stats Dashboard</h1>
    </header>
    
    <main>
      <router-view />
    </main>

    <footer>
      <p>NBA Stats Dashboard &copy; {{ new Date().getFullYear() }}</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  background-color: #1d428a;
  color: white;
  padding: 15px;
  text-align: center;
}

main {
  flex: 1;
  background-color: #f8f9fa;
}

footer {
  background-color: #1d428a;
  color: white;
  padding: 10px;
  text-align: center;
}
</style>
