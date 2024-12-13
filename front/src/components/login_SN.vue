<script>
import axios from "axios";
import {ElMessage} from "element-plus";
export default {
  data() {
    return{
      load:true,
      src:'',
      account:''
    }
  },
  mounted() {
    this.login();
    this.sendGetRequest();
  },
  methods:{
    skip(){
      const currentRoute = this.$route;
      this.$router.push({
        name:"JD",
        query:currentRoute.query
      })
    },
    sendGetRequest() {
      axios.get('/get_SN')
          .then(response => {
            this.src = response.data
            console.log(this.src)
            this.load=false
          })
    },
    login(){
      axios.get("/login_SN").then(response => {
        let message = response.data
        if(message==="success"){
          ElMessage.success("登录成功")
          const currentRoute = this.$route;
          this.$router.push({
            name:"JD",
            query:currentRoute.query
          })
        }else {
          ElMessage.error("登录失败")
        }
      })
    }
  },
}
</script>

<template>
  <div class="all">
    <div class="form">
      <div  class="name">
        <h1 class="title">Login</h1>
        <h1 class="title" style="color: #f5dd5d">苏宁</h1>
        <p class="login_font">请使用微信扫描下方的二维码登录</p>
      </div>
      <div v-loading="load"  class="img">
        <img v-if="src.length!==0" class="login_img" :src="src" :alt=0>
      </div>
      <el-button class="card_button" @click="skip()">
        <span class="font">Skip</span>
      </el-button>
      <div class="background">
        <span class="shape shape4"></span>
        <span class="shape shape3"></span>
        <span class="shape shape2"></span>
        <span class="shape shape1"></span>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet');
.name{
  position: absolute;
  z-index: 2;
  margin-top: 10%;
  margin-left: 3%;
}
.title{
  font-family: 'Montserrat', sans-serif;
  color: #0b59cf;
  font-size: 40px;
  font-style: italic;
  font-weight: 900;
  letter-spacing: 2px;
}
.all{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('./icons/low-poly-grid-haikei.svg');
  background-repeat: no-repeat;
  background-position: right bottom;
  background-size: cover;
}
.img{
  position: absolute;
  width: 200px;
  height: 200px;
  margin-top: 60%;
  margin-left:20%;
  z-index: 2;
}
.form{
  position: relative;
  background-color: rgba(255, 255, 255, 0.5);
  top:50%;
  left:50%;
  width: 430px;
  height: 620px;
  transform: translate(-50%, -50%);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.form:hover {
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
}
.background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 430px;
  height: 620px;
  z-index: 1;
  overflow: hidden;
}
.shape {
  transform: rotate(45deg);
  position: absolute;
}
.shape1 {
  height: 550px;
  width: 720px;
  background: #FFF;
  top: -20px;
  right: 80px;
  border-radius: 0 72px 0 0;
}
.shape2 {
  height: 200px;
  width: 300px;
  background: #3875d7;
  top: -180px;
  right: 60px;
  border-radius: 32px;
}
.shape3 {
  height: 640px;
  width: 300px;
  background: linear-gradient(270deg, #5897fb, #003366);
  top: -80px;
  right: -65px;
  border-radius: 32px;
}
.shape4 {
  height: 250px;
  width: 200px;
  background: #3875d1;
  top: 430px;
  right: -100px;
  border-radius: 60px;
}
.login_font{
  font-family: 'Montserrat', sans-serif;
  color: #000000;
  margin-top: 30px;
  font-size: 15px;
  font-style: italic;
  font-weight: 900;
  letter-spacing: 2px;
}
.login_img{
  margin-top: 5%;
  margin-left: 5%;
  height: 90%;
  width: 90%;
  border: 1px solid #333;
  box-shadow: 10px 10px 5px rgba(0, 0, 0, 0.3);
  transition: transform 0.5s ease, border-color 0.5s ease;
}
.font{
  font-family: 'Montserrat', sans-serif;
  color: #000000;
  font-size: 15px;
  font-style: italic;
  font-weight: 900;
  letter-spacing: 2px;
}
.login_img:hover {
  transform: scale(1.1);
}
.card_button {
  position: absolute;
  margin-top: 570px;
  margin-left: 5%;
  width: 80px;
  transition: .2s;
  z-index: 3;
  background: #fff;
  border-radius: 26px;
  border: 2px solid #0b59cf;
  box-shadow: 0 4px 16px rgb(10, 64, 165,0.2);
  color: #2d81c8;
}
.card_button:active,
.card_button:focus,
.card_button:hover {
  background-color: #ffffff;
  transition: box-shadow 0.3s ease;
  color: #2f4a78;
  border-color: #2861bf;
  box-shadow: 0 4px 16px rgba(40, 97, 191, 0.6);
  border-width: 3px;
}
@media (max-width: 500px) {
  .form{
    position: relative;
    top:50%;
    left:50%;
    width: 360px;
    height: 620px;
    transform: translate(-50%, -50%);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  .form:hover {
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
  }
  .background {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 360px;
    height: 620px;
    z-index: 1;
    overflow: hidden;
  }
  .shape {
    transform: rotate(45deg);
    position: absolute;
  }
  .shape1 {
    height: 550px;
    width: 720px;
    background: #FFF;
    top: -20px;
    right: 80px;
    border-radius: 0 72px 0 0;
  }
  .shape2 {
    height: 200px;
    width: 300px;
    background: #3875d7;
    top: -180px;
    right: 60px;
    border-radius: 32px;
  }
  .shape3 {
    height: 640px;
    width: 300px;
    background: linear-gradient(270deg, #5897fb, #003366);
    top: -80px;
    right: -65px;
    border-radius: 32px;
  }
  .shape4 {
    height: 250px;
    width: 200px;
    background: #3875d1;
    top: 430px;
    right: -100px;
    border-radius: 60px;
  }
}
</style>