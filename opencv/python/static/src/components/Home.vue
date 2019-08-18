<template lang="pug">
.home
  h1.title.has-text-centered circle
  .file
    label.file-label
      input.file-input(type="file" ref="file" @change="file_change")
      span.file-cta
        span.file-icon
          i.fas.fa-upload
        span.file-label(v-if="filename") {{filename}}
        span.file-label(v-else) Choose a file…
    button.button.is-primary(v-if="filename" @click="upload") upload
  img.image.p-t-3(:src="url" v-if="url")

</template>

<script>
import axios from 'axios'
export default {
  name:'Home',
  data() {
    return {
      filename:null,
      url:null
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
        this.url=axios.defaults.baseURL+"/uploads/gray.png?" + new Date().getTime();
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