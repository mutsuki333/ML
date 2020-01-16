<template lang="pug">
.home
  h1.title.has-text-centered circle
  .buttons.is-centered
    button.button.is-info(@click="left") left
    button.button.is-info(@click="clear") clear
    button.button.is-info(@click="right") right
  .file
    button.button.is-primary(@click="capture") capture
    p.p-x-2 or
    label.file-label
      input.file-input(type="file" ref="file" @change="file_change")
      span.file-cta
        span.file-icon
          i.fas.fa-upload
        span.file-label(v-if="filename") {{filename}}
        span.file-label(v-else) Choose a file…
    button.button.is-primary(v-if="filename" @click="upload") upload
  img.image.p-t-3(:src="upload_pic" v-if="upload_pic")
  div.p-b-5(v-if="results")
    h3.p-t-2.subtitle results
    .table_container
      table.table.is-striped.is-bordered
        thead
          tr
            th(v-for="item in results.title") {{item}}
        tbody
          tr
            td(v-for="item in results.url")
              img.image(:src="item")
          tr
            td(v-for="item in results.fit" v-if="item.length>0")
              h3 ellipse 1
              | center : {{item[0][0]}} 
              br
              | size: {{item[0][1]}}
              br
              br
              h3 ellipse 2
              | center : {{item[1][0]}}
              br
              | size: {{item[1][1]}}
            td(v-else)
  
              



</template>

<script>
import axios from 'axios'
export default {
  name:'Home',
  data() {
    return {
      filename:null,
      url:null,
      upload_pic:null,
      results:null
    }
  },
  created() {
  },
  methods: {
    file_change(){
      if(this.$refs.file.files.length > 0){
        this.filename=this.$refs.file.files[0].name
      }
      else this.filename=null
    },
    left(){
      axios('/control/left')
    },
    right(){
      axios('/control/right')
    },
    clear(){
      axios('/control/clear')
    },
    capture(){
      axios('/cam')
      .then(res=>{
        this.results = res.data
        this.upload_pic = axios.defaults.baseURL+"/uploads/capture.jpg" + "?" + new Date().getTime();
        for (let obj in this.results) {
          this.results[obj].url = `${axios.defaults.baseURL}/uploads/${this.results[obj].title}.png?` + new Date().getTime();
        }
        //restructure
        let tmp = {title:[],url:[],fit:[]}
        for(let obj in this.results){
          tmp.title.push(this.results[obj].title)
          tmp.url.push(this.results[obj].url)
          tmp.fit.push(this.results[obj].fit)
        }
        this.results = tmp
      })
    },
    upload(){
      let formData = new FormData();
      formData.append('file', this.$refs.file.files[0]);
      axios.post('/upload',formData,{
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(res=>{
        console.log(res)
        this.results = res.data
        this.upload_pic = axios.defaults.baseURL+"/uploads/"+this.filename + "?" + new Date().getTime();
        console.log(this.results)
        for (let obj in this.results) {
          this.results[obj].url = `${axios.defaults.baseURL}/uploads/${this.results[obj].title}.png?` + new Date().getTime();
        }

        //restructure
        let tmp = {title:[],url:[],fit:[]}
        for(let obj in this.results){
          tmp.title.push(this.results[obj].title)
          tmp.url.push(this.results[obj].url)
          tmp.fit.push(this.results[obj].fit)
        }
        this.results = tmp

      })
    }
  },
}
</script>

<style lang="sass" scoped>
.home
  position: relative
  width: 60%
  left: 20%
</style>