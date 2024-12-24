<script>
import {Document, HomeFilled, Setting, ShoppingCartFull, User, UserFilled} from "@element-plus/icons-vue";
import axios from "axios";

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
      downs:[
        {
          form:'京东',
          title:'1',
          pre_price:1000,
          rec_price:100,
        },
      ]
    }
  },
  mounted() {
    this.checkWidth();
    window.addEventListener('resize', this.checkWidth);
  },
  created() {
    this.account = this.$route.query.account;
    console.log('Received account:', this.account);
    this.get_em();
    this.down();
  },
  methods: {
    checkWidth() {
      this.shouldShow = window.innerWidth >= 500;
    },
    get_em(){
      axios.post("/get_account",
          {
            "account":this.account,
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
            "account":this.account,
          }).then(response => {
        this.downs = response.data;
      })
    },
    quit(){
      localStorage.removeItem(`authToken_${this.account}`);
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
    <el-container v-if="shouldShow">
      <el-aside  class="aside">
        <el-menu
            default-active="3"
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
          <div class="down2" v-loading.body.lock="downs[0].title==='1'" v-for="obj in downs" >
            <el-alert v-if="(obj.rec_price/obj.pre_price) <= 0.6 && obj.rec_price!==0" type="success">
              <div>
                <p class="text" style="color: #199c2d; font-size: 15px">大减价！！</p>
                <span class="text">您从{{obj.from}}关注的商品:<br>{{obj.title}}<br> 从 ￥</span>
                <span class="text" style="color: #199c2d;">{{obj.pre_price}}</span>
                <span class="text"> 降价到了 ￥</span>
                <span class="text" style="color: #f10404;">{{obj.rec_price}}</span>
                <span class="text"> !快去看看吧！！！</span>
              </div>
            </el-alert>
            <el-alert v-else-if="(obj.rec_price/obj.pre_price) <= 0.9 && obj.rec_price!==0" type="warning">
              <div>
                <p class="text" style="color: #ff9100; font-size: 15px">价格优惠！！</p>
                <span class="text">您从{{obj.from}}关注的商品:<br>{{obj.title}}<br> 从 ￥</span>
                <span class="text" style="color: #eab778;">{{obj.pre_price}}</span>
                <span class="text"> 降价到了 ￥</span>
                <span class="text" style="color: #ff9100;">{{obj.rec_price}}</span>
                <span class="text"> !快去看看吧！！！</span>
              </div>
            </el-alert>
            <el-alert v-else-if="obj.rec_price!==0" type="info">
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
          <p class="text mat">注册时间：{{user.date_joined}}</p>
          <el-button  class="card_button" @click="quit()">
            <span class="text_button">退出登录</span>
          </el-button>
        </div>
      </div>
    </el-main>
    <el-container v-if="!shouldShow" class="bottom">
      <el-menu
          default-active="3"
          class="el-menu-horizontal-demo"
          :collapse="isCollapse"
          mode="horizontal"
          :router="true"
      >
        <el-menu-item  @click="changeRoute('/main')" index="1" class="icon">
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
    </el-container>
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
    left: 0;
    width: 100%;
    height:84vh;
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
  .background{
    position: absolute;
    width: 800px;
    height: 500px;
    bottom: 0;
    right: 0;
    z-index: 0;
    transform: scaleY(-1);
  }
  .bottom{
    position: absolute;
    top: 92vh;
    left: 0;
    height:7vh;
    width: 100%;
  }
  .el-menu-horizontal-demo{
    width: 100%;
    margin-left: 3%;
    margin-right: 3%;
    height: 100%;
  }
  .icon{
    margin-left: 13% !important;
  }
  .avatar{
    margin-left: 15px;
    margin-top: 15px;
    height: 60px;
    width: auto;
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
    width: 60px;
    margin-top: 10px;
    border-radius: 8px;
    border: 1px solid #0b59cf;
    box-shadow: 0 2px 10px rgb(10, 64, 165,0.2);
    transition: .2s;
    color: #f5f7f8;
    margin-left: 220px;
  }
  .text_button{
    font-family: 'Montserrat', sans-serif;
    font-size: 12px;
    font-style: italic;
    font-weight: 900;
    letter-spacing: 2px;
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