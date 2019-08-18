<template lang="pug">
#app
  router-view 
</template>

<script>
import "src/theme.sass"
import 'babel-polyfill'

export default {
  name: "App",
  created() {
    console.log("app");
  },
  metaInfo: {
    // if no subcomponents specify a metaInfo.title, this title will be used
    title: 'Circle',
    // all titles will be injected into this template
    titleTemplate: '%s | 專題'
  }
}

</script>

<style lang="sass" scoped>
#app
  font-family: 'Avenir', Helvetica, Arial, sans-serif
  -webkit-font-smoothing: antialiased
  -moz-osx-font-smoothing: grayscale
  // text-align: center
  color: #2c3e50

</style>