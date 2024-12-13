<script>
import {Lock, Message, User} from "@element-plus/icons-vue";
import axios from "axios";
import {ElMessage} from "element-plus";
export default {
  components: {Message, User, Lock},
  data() {
    return {
      account: '',
      password:'',
      new_acc:1,
      new_account:'',
      new_password:'',
      new_email:''
    };
  },
  created() {
    this.account = this.$route.query.account;
    console.log('Received account:', this.account);
  },
  methods:{
    Login(){
      axios.post("/login",
          {
            account:this.account,
            password:this.password
          }).then(response => {
        let message = response.data
        if (message.includes("success")) {
          ElMessage.success(message)
          this.$router.push({
            name:"A",
            query:{
              account:this.account
            }
          })
        } else {
          ElMessage.error(message)
        }
      })
      console.log('用户输入的内容是：', this.account,this.password);
    },
    register(){
      let regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      let emailValid = regex.test(this.new_email);
      if(this.new_account.length<=6){
        ElMessage.error("请保证账号至少有六位！")
      }else if(!emailValid){
        ElMessage.error("请输入正确格式邮箱！")
      }else if(this.new_password.length<=6){
        ElMessage.error("请保证密码至少有六位！")
      }
      else{
        axios.post("/login/register",
            {
              account:this.new_account,
              email:this.new_email,
              password:this.new_password
            }).then(response => {
          let message = response.data
          if (message.includes("success")) {
            this.new_acc=1
            ElMessage.success(message)
          } else {
            ElMessage.error(message)
          }
        })
      }
    }
  }
}
</script>



<template>
  <div class="all">
    <div class="form">
      <div v-if="new_acc===1" class="name">
        <h1 class="title">Price<br> Sleuth</h1>
      </div>
      <form  v-if="new_acc===1" class="form_input">
        <div class="login">
          <el-icon style="color: #3875d7"><User /></el-icon>
          <input v-model="account" type="text" class="input" placeholder="Account"/>
        </div>
        <div class="login">
          <el-icon style="color: #3875d7"><Lock /></el-icon>
          <input v-model="password" type="password" class="input" placeholder="Password">
        </div>
        <el-button class="button" @click="Login">
          <span class="text">Log In Now</span>
        </el-button>
        <br>
        <el-button class="button new_account" @click="new_acc=0,account='',password=''">
          <span class="text">Register</span>
        </el-button>
      </form>
      <form  v-if="new_acc===0" class="form_input new">
        <div class="login">
          <el-icon style="color: #3875d7"><User /></el-icon>
          <input v-model="new_account" type="text" class="input" placeholder="Please Input your account"/>
        </div>
        <div class="login">
          <el-icon style="color: #3875d7"><Message /></el-icon>
          <input v-model="new_email" type="email" class="input" placeholder="Please Input your email">
        </div>
        <div class="login">
          <el-icon style="color: #3875d7"><Lock /></el-icon>
          <input v-model="new_password" type="password" class="input" placeholder="Please Input your Password">
        </div>
        <el-button class="button" @click="register">
          <span class="text">Register Now</span>
        </el-button>
        <br>
        <el-button class="button new_account" @click="new_acc=1,new_password='',new_account='',new_email=''">
          <span class="text">Back To Login</span>
        </el-button>
      </form>
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
.new{
  margin-top: -100px;
}
.name{
  position: absolute;
  z-index: 2;
  margin-top: 10%;
  margin-left: 3%;
}
.title{
  font-family: 'Montserrat', sans-serif;
  color: #0b59cf;
  font-size: 75px;
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
.form_input{
  position: absolute;
  width: 100%;
  height: 100%;
  padding-top: 65%;
  padding-right: 10%;
  z-index: 2;
}
.login{
  padding-top: 5%;
  padding-left: 10%;
}
.form{
  position: relative;
  background-color: rgba(255, 255, 255, 0.5);
  top:50%;
  left:50%;
  width: 480px;
  height: 620px;
  transform: translate(-50%, -50%);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.form:hover {
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
}
.input {
  font-size: 18px;
  border: none;
  border-bottom: 2px solid #464646;
  width: 80%;
  background: none !important;
  padding: 5% 3% 1%;
  font-weight: 700;
  transition: .2s;
}
.input:active,
.input:focus,
.input:hover {
  outline: none;
  border-bottom-color: #3875d7;
}


.background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 480px;
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

.button {
  background: #fff;
  margin-top: 10%;
  margin-left: 30%;
  padding: 20px;
  border-radius: 26px;
  border: 2px solid #0b59cf;
  display: flex;
  align-items: center;
  width: 70%;
  box-shadow: 0 4px 16px rgb(10, 64, 165,0.2);
  transition: .2s;
  color: #2d81c8;
}
.button:active,
.button:focus,
.button:hover {
  background-color: #ffffff;
  transition: box-shadow 0.3s ease;
  color: #2f4a78;
  border-color: #2861bf;
  box-shadow: 0 4px 16px rgba(40, 97, 191, 0.6);
  border-width: 3px;
}
.new_account{
  margin-top: 4px;
}
.text{
  font-weight: 700;
  text-transform: uppercase;
}
@media (max-width: 500px) {
  .form{
    position: relative;
    background-color: #74caf4;
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