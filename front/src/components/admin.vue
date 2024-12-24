<script >
import {Document, HomeFilled, Setting, ShoppingCartFull, User, UserFilled} from "@element-plus/icons-vue";
import axios from "axios";
import {ElMessage} from "element-plus";

export default {
  components: {User, ShoppingCartFull, UserFilled, HomeFilled, Setting, Document},
  data(){
    return{
      shouldShow: true,
      account:'',
      isCollapse:true,
      user:{
        account:'Emdiso717',
        email:'111111111@email.com'
      },
      send:false
    }
  },
  created() {
    this.account = this.$route.query.account;
    console.log('Received account:', this.account);
    this.get_em();
  },

  mounted() {
    this.checkWidth();
    window.addEventListener('resize', this.checkWidth);
  },
  methods: {
    checkWidth() {
      this.shouldShow = window.innerWidth >= 500;
    },
    changeRoute(path) {
      const currentRoute = this.$route;
      this.$router.push({
        path: path,
        query: currentRoute.query
      });
    },
    check(){
      axios.post("/new_price").then(response => {
        ElMessage.success(response.data);

      })
      this.send=true
    },
    get_em(){
      axios.post("/get_account",
          {
            "account":this.account,
          }).then(response => {
        this.user = response.data;
      })
    },
    quit() {
      localStorage.removeItem(`authToken_${this.account}`);
      this.$router.push({
        path: '/login',
      });
    },
    send_email(){
      axios.post("/send").then(response => {
        ElMessage.success(response.data);
      })
    }

  }
}
</script>

<template>
  <el-container class="all">
    <el-header class="header">
      <p class="title">Price  Sleuth</p>
    </el-header>
      <el-main class="main">
        <img class="background" src="./icons/cool-background%20.svg" alt="Description" />
        <div class="card">
          <p class="font">Userinfo</p>
          <el-avatar class="avatar"><img src="./icons/ad.jpg" alt="me"/></el-avatar>
          <p class="form_font po1">用户名：{{user.account}}</p>
          <p class="form_font po1 po2">用户名：{{user.email}}</p>
          <el-divider class="divider" />
          <div class="down" >
            <el-carousel v-if="!shouldShow" class="car" type="card" direction="vertical">
              <el-carousel-item >
                <img style="height: 100%;width: auto;" src="./icons/admin.jpg" alt="没东西了"/>
              </el-carousel-item>
              <el-carousel-item >
                <img style="height: 100%;width: auto;" src="./icons/admin1.jpg" alt="没东西了"/>
              </el-carousel-item>
              <el-carousel-item >
                <img style="height: 100%;width: auto;" src="./icons/admin2.jpg" alt="没东西了"/>
              </el-carousel-item>
            </el-carousel>
            <el-carousel v-if="shouldShow" class="car" type="card" >
              <el-carousel-item >
                <img style="height: 100%;width: auto;" src="./icons/admin.jpg" alt="没东西了"/>
              </el-carousel-item>
              <el-carousel-item >
                <img style="height: 100%;width: auto;" src="./icons/admin1.jpg" alt="没东西了"/>
              </el-carousel-item>
              <el-carousel-item >
                <img style="height: 100%;width: auto;" src="./icons/admin2.jpg" alt="没东西了"/>
              </el-carousel-item>
              <el-carousel-item >
                <img style="height: 100%;width: auto;" src="./icons/admin3.jpg" alt="没东西了"/>
              </el-carousel-item>
            </el-carousel>
            <p class="text mat">注册时间：{{user.date_joined}}</p>
            <el-row type="flex" justify="start" align="middle">
              <el-col :span="8">
                <el-button class="card_button" @click="check()">
                  <span class="text_button">check price</span>
                </el-button>
              </el-col>
              <el-col :span="8" >
                <el-button  v-if="send" class="card_button" @click="send_email()">
                  <span class="text_button">send email</span>
                </el-button>
              </el-col>
              <el-col :span="8">
                <el-button class="card_button" @click="quit()">
                  <span class="text_button">quit</span>
                </el-button>
              </el-col>
            </el-row>
          </div>
        </div>
      </el-main>
  </el-container>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet');
.all{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
.car{
  position:relative;
  height: 88%;
  width: auto;
  z-index: 1;
}
.header{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 8vh;
  background: linear-gradient(#66ace6, #d5e3e8);
}
.card{
  position:relative;
  margin-left: 10%;
  width: 80%;
  height: 100%;
  transition: box-shadow 0.3s ease-in-out;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  z-index: 1;
  background-color: rgba(255, 255, 255, 0.5);
}
.card:hover {
  box-shadow: 0 16px 32px rgba(0, 0, 0, 0.4);
}
.background{
  position: absolute;
  width: 100%;
  height: auto;
  bottom: 0;
  right: 0;
  z-index: 0;
  transform: scaleY(-1);
}
.title{
  font-family: 'Montserrat', sans-serif;
  color: #0b59cf;
  font-size: 300%;
  font-style: italic;
  font-weight: 900;
  letter-spacing: 2px;
  margin-bottom: 1%;
}
.main{
  position: absolute;
  top: 8vh;
  left: 0;
  width: 100%;
  height: 92%;
}
.divider{
  position: relative;
  top:-80px;
  margin-left: 10%;
  width: 80%;
}
.down{
  position: relative;

  top:-70px;
  width: 80%;
  margin-left: 10%;
  height: 58%;
}
.down2{
  margin-top: 10px;
}
.text{
  font-family: 'Montserrat', sans-serif;
  color: #000000;
  font-size: 13px;
  font-style: italic;
  font-weight: 600;
  letter-spacing: 2px;
}
.card_button {
  background-color: #0b59cf;
  margin-top: 50px;
  border-radius: 8px;
  border: 1px solid #0b59cf;
  box-shadow: 0 2px 10px rgb(10, 64, 165,0.2);
  transition: .2s;
  color: #f5f7f8;
  margin-left: 20px;
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
.text_button{
  font-family: 'Montserrat', sans-serif;
  font-size: 14px;
  font-style: italic;
  font-weight: 900;
  letter-spacing: 2px;
}
.font{
  font-family: 'Montserrat', sans-serif;
  color: #0b59cf;
  font-size: 30px;
  font-style: italic;
  font-weight: 900;
  letter-spacing: 2px;
  text-align: center;
}
.po1{
  position: relative;
  top:-80px;
  left: 200px;
}
.po2{
  margin-top: 10px;
}
.avatar{
  margin-left: 60px;
  margin-top: 30px;
  height: 80px;
  width: auto;
}
.form_font{
  font-family: 'Montserrat', sans-serif;
  color: #000000;
  font-size: 20px;
  font-style: italic;
  font-weight: 900;
  letter-spacing: 2px;
}

@media (max-width: 500px) {
  .main{
    position: absolute;
    top: 8vh;
    left: 0vw;
    width: 100%;
    height:92%;
  }
  .background{
    position: absolute;
    width: 800px;
    height: 500px;
    bottom: 0;
    right: 0;
    z-index: 0;
    transform: scaleY(-1);
  }
  .card{
    position:relative;
    margin-left: 2.5%;
    width: 95%;
    height: 100%;
    transition: box-shadow 0.3s ease-in-out;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    z-index: 1;
    background-color: rgba(255, 255, 255, 0.5);
  }
  .card:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }

  .avatar{
    margin-left: 15px;
    margin-top: 15px;
    height: 60px;
    width: 60px;
  }
  .form_font{
    font-family: 'Montserrat', sans-serif;
    color: #000000;
    font-size: 13px;
    font-style: italic;
    font-weight: 900;
    letter-spacing: 1px;
    width: 73%;
  }
  .po1{
    position: relative;
    top:-60px;
    left: 85px;
  }
  .po2{
    margin-top: 10px;
  }
  .down{
    position: relative;
    top:-80px;
    width: 90%;
    margin-left: 5%;
    height: 60%;
  }
  .text{
    font-family: 'Montserrat', sans-serif;
    color: #000000;
    font-size: 10px;
    font-style: italic;
    font-weight: 600;
    letter-spacing: 1px;
  }
  .mat{
    margin-top: 10px;
  }
  .card_button {
    background-color: #0b59cf;
    margin-top: 30px;
    border-radius: 8px;
    border: 0 solid #0b59cf;
    box-shadow: 0 2px 10px rgb(10, 64, 165,0.2);
    transition: .2s;
    color: #f5f7f8;
    margin-left: 2px;
  }
  .text_button{
    font-family: 'Montserrat', sans-serif;
    font-size: 9px;
    font-style: italic;
    font-weight: 800;
    letter-spacing: 1px;
    margin-left: -3px;
    margin-right: -3px;
  }
  .font{
    font-family: 'Montserrat', sans-serif;
    color: #0b59cf;
    font-size: 20px;
    font-style: italic;
    font-weight: 900;
    letter-spacing: 2px;
    text-align: center;
  }
}
</style>