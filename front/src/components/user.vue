<script>
import {Document, HomeFilled, Setting, ShoppingCartFull, User, UserFilled} from "@element-plus/icons-vue";
import axios from "axios";

export default {
  components: {User, ShoppingCartFull, UserFilled, HomeFilled, Setting, Document},
  data(){
    return{
      account:'',
      isCollapse:true,
      user:{
        account:'Emdiso717',
        email:'111111111@email.com'
      },
      downs:[
        {
          form:'京东',
          title:'111111111111111111111',
          pre_price:1000,
          rec_price:100,
        },
        {
          form:'京东',
          title:'111111111111111111111',
          pre_price:1000,
          rec_price:100,
        },
        {
          form:'京东',
          title:'111111111111111111111',
          pre_price:1000,
          rec_price:100,
        },
        {
          form:'京东',
          title:'111111111111111111111',
          pre_price:1000,
          rec_price:100,
        },
        {
          form:'京东',
          title:'111111111111111111111',
          pre_price:1000,
          rec_price:100,
        },
        {
          form:'京东',
          title:'33333',
          pre_price:1000,
          rec_price:700,
        },
        {
          form:'京东',
          title:'22222222222',
          pre_price:1000,
          rec_price:980,
        }
      ]
    }
  },
  created() {
    this.account = this.$route.query.account;
    console.log('Received account:', this.account);
    this.get_em();
    this.down();
  },
  methods: {
    get_em(){
      axios.post("/get_account",
          {
            account:this.account,
          }).then(response => {
        this.user = response.data;
      })
    },
    changeRoute(path) {
      const currentRoute = this.$route;
      this.$router.push({
        path: path,
        query: currentRoute.query
      });
    },
    down(){
      axios.post("/down",
          {
            account:this.account,
          }).then(response => {
        this.downs = response.data;
      })
    },
    quit(){
      this.$router.push({
        path: '/login',
      });
    }
  }
}
</script>

<template>
  <el-container class="all">
    <el-header class="header">
      <p class="title">Price  Sleuth</p>
    </el-header>
    <el-container>
      <el-aside  class="aside">
        <el-menu
            default-active="2"
            class="el-menu-vertical-demo"
            :collapse="isCollapse"
            :router="true"
        >
          <el-menu-item  @click="changeRoute('/main')" index="main" class="icon">
            <el-icon style="color: black"><HomeFilled /></el-icon>
            <template #title>商品搜索</template>
          </el-menu-item>
          <el-menu-item @click="changeRoute('/car')" index="2" class="icon">
            <el-icon style="color: black"><ShoppingCartFull /></el-icon>
            <template #title>购物车</template>
          </el-menu-item>
          <el-menu-item @click="changeRoute('/user')" index="3" class="icon">
            <el-icon style="color: black"><User /></el-icon>
            <template #title>个人信息</template>
          </el-menu-item>
        </el-menu>
      </el-aside>
    </el-container>
    <el-main class="main">
      <img class="background" src="./icons/cool-background%20.svg" alt="Description" />
      <div class="card">
        <p class="font">Userinfo</p>
        <el-avatar
            src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" class="avatar"
        />
        <p class="form_font po1">用户名：{{user.account}}</p>
        <p class="form_font po1 po2">用户名：{{user.email}}</p>
        <el-divider class="divider" />
        <div class="down" >
          <el-scrollbar >
          <div class="down2" v-for="obj in downs" >
            <el-alert v-if="(obj.rec_price/obj.pre_price) <= 0.6" type="success">
              <div>
                <p class="text" style="color: #199c2d; font-size: 15px">大减价！！</p>
                <span class="text">您从{{obj.from}}关注的商品:<br>{{obj.title}}<br> 从 ￥</span>
                <span class="text" style="color: #199c2d;">{{obj.pre_price}}</span>
                <span class="text"> 降价到了 ￥</span>
                <span class="text" style="color: #f10404;">{{obj.rec_price}}</span>
                <span class="text"> !快去看看吧！！！</span>
              </div>
            </el-alert>
            <el-alert v-else-if="(obj.rec_price/obj.pre_price) <= 0.9" type="warning">
              <div>
                <p class="text" style="color: #ff9100; font-size: 15px">价格优惠！！</p>
                <span class="text">您从{{obj.from}}关注的商品:<br>{{obj.title}}<br> 从 ￥</span>
                <span class="text" style="color: #eab778;">{{obj.pre_price}}</span>
                <span class="text"> 降价到了 ￥</span>
                <span class="text" style="color: #ff9100;">{{obj.rec_price}}</span>
                <span class="text"> !快去看看吧！！！</span>
              </div>
            </el-alert>
            <el-alert v-else type="info">
              <div>
                <p class="text" style="color: gray; font-size: 15px">小幅降价！</p>
                <span class="text">您从{{obj.from}}关注的商品:<br>{{obj.title}}<br> 从 ￥</span>
                <span class="text" style="color: #131313;">{{obj.pre_price}}</span>
                <span class="text"> 降价到了 ￥</span>
                <span class="text" style="color:  #000000;">{{obj.rec_price}}</span>
                <span class="text"> !快去看看吧！！！</span>
              </div>
            </el-alert>
          </div>
          </el-scrollbar>
          <p class="text">注册时间：{{user.date_joined}}</p>
          <el-button  class="card_button" @click="quit()">
            <span class="text_button">退出登录</span>
          </el-button>
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
.header{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 8vh;
  background: linear-gradient(#66ace6, #d5e3e8);
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
.aside{
  position: absolute;
  top: 8vh;
  left: 0;
  height: 92vh;
  width: 4vw;
  background-color: #0b59cf;
}
.el-menu-vertical-demo{
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
}
.icon{
  margin-top: 20%;
}
.main{
  position: absolute;
  top: 8vh;
  left: 4vw;
  width: 96%;
  height: 92%;
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
  width: 80px;
  margin-top: 10px;
  border-radius: 8px;
  border: 1px solid #0b59cf;
  box-shadow: 0 2px 10px rgb(10, 64, 165,0.2);
  transition: .2s;
  color: #f5f7f8;
  margin-left: 1000px;
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
@media (max-width: 500px) {
  .aside{
    position: absolute;
    top: 8vh;
    left: 0;
    height:92vh;
    width: 12vw;
  }
  .main{
    position: absolute;
    top: 8vh;
    left: 12vw;
    width: 88%;
    height:92%;
  }
  .card{
    margin-left: 2%;
    width: 96%;
    height: 100%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  .card:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
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
}
</style>