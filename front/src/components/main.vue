<script >
import {Document, HomeFilled, Setting, ShoppingCartFull, User, UserFilled} from "@element-plus/icons-vue";
import axios from "axios";
import {ElMessage} from "element-plus";

export default {
  components: {User, ShoppingCartFull, UserFilled, HomeFilled, Setting, Document},
  data(){
    return{
      account:'',
      isCollapse:true,
      search:'',
    }
  },
  created() {
    this.account = this.$route.query.account;
    console.log('Received account:', this.account);
  },
  methods: {
    changeRoute(path) {
      const currentRoute = this.$route;
      this.$router.push({
        path: path,
        query: currentRoute.query
      });
    },
    Search(){
      axios.post("/search",
          {
            search:this.search
          }).then(response => {
        let message = response.data
        if (message.includes("success")) {
          ElMessage.success(message)}
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
          <div class="search-box">
            <form class="inline">
              <input v-model="search" type="text" class="input" placeholder="搜一下就知道！">
              <el-button class="button" @click="Search">
                <span class="text">Search</span>
              </el-button>
            </form>
          </div>
        <div class="commodity">
          <el-card class="good_card">
            <p v-for="o in 4" :key="o" class="text item">{{ 'List item ' + o }}</p>
          </el-card>
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
.inline{
  display: flex;
  align-items: center;
}
.search-box{
  position: absolute;
  margin-left: 18vw;
  margin-top: 1%;
  width: 60%;
  height: 10%;
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
.input {
  font-size: 16px;
  border: 2px solid #464646;
  width: 90vw;
  background: none;
  padding: 1.5% 3% 1.5% 3%;
  font-weight: 600;
  transition: .2s;
  border-radius: 5px;
}
.input:active,
.input:focus,
.input:hover {
  outline: none;
  border-color: #6897e3;
}
.button {
  background-color: #0b59cf;
  margin-left: 1%;
  padding: 2.5% 0.5%;
  width: 10vw;
  border-radius: 10px;
  border: 2px solid #0b59cf;
  box-shadow: 0 4px 16px rgb(10, 64, 165,0.2);
  transition: .2s;
  color: #f5f7f8;
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
.text{
  font-size:2vh;
  font-weight: 600;
  text-transform: uppercase;
}
.commodity{
  position: absolute;
  top: 15%;
  left: 3%;
  width: 93%;
  min-height:82%;
}
.good_card{
  width: 35%;
  height: 40%;
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
  .search-box{
    position: absolute;
    margin-left: 2vw;
    margin-top: 1%;
    width: 50%;
    height: 10%;
  }
  .input {
    font-size: 14px;
    border: 2px solid #464646;
    width: 90vw;
    background: none;
    padding: 4% 3% 4% 3%;
    font-weight: 600;
    transition: .2s;
    border-radius: 5px;
  }
  .input:active,
  .input:focus,
  .input:hover {
    outline: none;
    border-color: #6897e3;
  }
  .button {
    background-color: #0b59cf;
    margin-left: 2%;
    padding: 2.5% 0.5%;
    width: 20vw;
    border-radius: 10px;
    border: 2px solid #0b59cf;
    box-shadow: 0 4px 16px rgb(10, 64, 165,0.2);
    transition: .2s;
    color: #f5f7f8;
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
}
</style>