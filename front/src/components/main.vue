<script xmlns="http://www.w3.org/1999/html">
export default {
  data(){
    return{
      account:''
    }
  },
  created() {
    this.account = this.$route.query.account;
    console.log('Received account:', this.account);
  }
}
</script>

<template>
  <div class="all">
    <el-header>Header</el-header>

  </div>
</template>

<style scoped>
.all{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>