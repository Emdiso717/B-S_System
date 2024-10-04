<script>
import {Document, HomeFilled, Setting, ShoppingCartFull, User, UserFilled} from "@element-plus/icons-vue";

export default {
  components: {User, ShoppingCartFull, UserFilled, HomeFilled, Setting, Document},
  data(){
    return{
      account:'',
      isCollapse:true
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
      <el-scrollbar height="100%">
      </el-scrollbar>
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
.aside{
  position: absolute;
  top: 8vh;
  left: 0;
  height: 92vh;
  width: 8vh;
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
  left: 8vh;
  width: 92%;
  height: 92%;
}
</style>