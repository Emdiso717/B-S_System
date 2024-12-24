<script >
import {Document, HomeFilled, Setting, ShoppingCartFull, User, UserFilled} from "@element-plus/icons-vue";
import axios from "axios";
import {ElNotification,ElMessage} from "element-plus";
export default {
  components: {User, ShoppingCartFull, UserFilled, HomeFilled, Setting, Document},
  data(){
    return{
      load:false,
      model:1,
      account:'',
      mainClass: 'main',
      isCollapse:true,
      search:'',
      filter:false,
      JD_search_goods:[],
      SN_search_goods:[],
      A_search_goods:[],
      fork_JD_good:{},
      fork_SN_good:{},
      fork_A_good:{},
      acc:true,
      filter_search:'',
      open_compare:false,
      shouldShow: true,
    }

  },
  created() {
    this.account = this.$route.query.account;
    console.log('Received account:', this.account);
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
    Search(){
      this.load=true;
      Promise.all([
        axios.post("/searchJD", {"search":this.search}),
        axios.post("/searchSN", {"search":this.search}),
        axios.post("/searchA", {"search":this.search}),
      ]).then(response => {
        const [response1, response2, response3] = response;
        let message1 = response1.data
        let message2 = response2.data
        if(message1.length ===0 && message2.length ===0){
          ElMessage.error("没有结果")
        }else {
          this.JD_search_goods=response1.data;
          this.SN_search_goods=response2.data;
          this.A_search_goods=response3.data;
        }
        this.load=false;
      })
    },
    add_car_JD(good){
      axios.post("/add",
          {
            "good_id":good.id,
            "good_from":'JD',
            "good_title":good.title,
            "good_link":good.link,
            "good_img":good.img,
            "account":this.account,
            "good_price":good.price
          }).then(response => {
        let message = response.data
        if(message.includes("success")){
          ElMessage.success("添加成功")
        }else {
          ElMessage.error(message)
        }
      })
    },
    add_car_SN(good){
      axios.post("/add",
          {
            "good_id":good.id,
            "good_from":'SN',
            "good_title":good.title,
            "good_link":good.link,
            "good_img":good.img,
            "account":this.account,
            "good_price":good.price
          }).then(response => {
        let message = response.data
        if(message.includes("success")){
          ElMessage.success("添加成功")
        }else {
          ElMessage.error(message)
        }
      })
    },
    add_car_A(good){
      axios.post("/add",
          {
            "good_id":good.id,
            "good_from":'A',
            "good_title":good.title,
            "good_link":good.link,
            "good_img":good.img,
            "account":this.account,
            "good_price":good.price
          }).then(response => {
        let message = response.data
        if(message.includes("success")){
          ElMessage.success("添加成功")
        }else {
          ElMessage.error(message)
        }
      })
    },
    changeStyle1() {

      this.filter=true;
      this.mainClass = 'main new-top';
    },
    changeStyle2(){
      this.filter=false;
      this.mainClass = 'main';
    },
    openLink(link){
      window.open(link);
    },
    JD_fork(good){
      if(Object.keys(this.fork_JD_good).length === 0){
        this.fork_JD_good = good;
      }else{
        ElMessage.error("请先清空筛选区")
      }
    },
    SN_fork(good){
      if(Object.keys(this.fork_SN_good).length === 0){
        this.fork_SN_good = good;
      }else{
        ElMessage.error("请先清空筛选区")
      }
    },
    A_fork(good){
      if(Object.keys(this.fork_A_good).length === 0){
        this.fork_A_good = good;
      }else{
        ElMessage.error("请先清空筛选区")
      }
    },
    sortProducts() {
      if(this.acc){
        this.JD_search_goods.sort((a, b) => parseFloat(a.price)-parseFloat(b.price));
        this.SN_search_goods.sort((a, b) => parseFloat(a.price)-parseFloat(b.price));
        this.A_search_goods.sort((a, b) => parseFloat(a.price)-parseFloat(b.price));
      }
      else{
        this.JD_search_goods.sort((a, b) => parseFloat(b.price)-parseFloat(a.price));
        this.SN_search_goods.sort((a, b) => parseFloat(b.price)-parseFloat(a.price));
        this.A_search_goods.sort((a, b) => parseFloat(b.price)-parseFloat(a.price));
      }

    this.acc=!this.acc
    },
    down(){
      axios.post("/down",
          {
            "account":this.account,
          }).then(response => {
        let message = response.data
        message.forEach((obj) => {
          ElNotification({
            title: '降价提醒',
            dangerouslyUseHTMLString: true,
            message : `<div><span style="font-family: 'Montserrat', sans-serif;color: #000000;font-size: 11px;font-style: italic;font-weight: 600;">您从${obj.from}关注的商品:<br>${obj.title}<br>从</span><span style="font-family: 'Montserrat', sans-serif;color: #2f92e8;font-size: 11px;font-style: italic;font-weight: 600;">  ${obj.pre_price}  </span><span style="font-family: 'Montserrat', sans-serif;color: #000000;font-size: 12px;font-style: italic;font-weight: 600;">降价到了</span><span style="font-family: 'Montserrat', sans-serif;color: #f10404;font-size: 12px;font-style: italic;font-weight: 600;">  ${obj.rec_price}   </span><span style="font-family: 'Montserrat', sans-serif;color: #000000;font-size: 11px;font-style: italic;font-weight: 600;">!快去看看吧！！！</span></div>`,
            type: 'success',
            offset: 10,
          });
        });
      })
    }
  },
  computed:{
    JD_search_goods() {
      return this.JD_search_goods.filter(data =>
          !this.filter_search ||
          data.title.toLowerCase().includes(this.filter_search.toLowerCase())
      );
      },
    SN_search_goods() {
      return this.SN_search_goods.filter(data =>
          !this.filter_search ||
          data.title.toLowerCase().includes(this.filter_search.toLowerCase())
      );
    },
    A_search_goods() {
      return this.A_search_goods.filter(data =>
          !this.filter_search ||
          data.title.toLowerCase().includes(this.filter_search.toLowerCase())
      );
    }
  },
  mounted() {
    this.checkWidth();
    window.addEventListener('resize', this.checkWidth);
    this.down()
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.checkWidth);
  },
}
</script>

<template>
    <el-container class="all">
      <el-header class="header">
        <p class="title">Price  Sleuth</p>
      </el-header>
      <el-container v-if="shouldShow">
      <el-aside  class="aside" >
        <el-menu
            default-active="1"
            class="el-menu-vertical-demo"
            :collapse="isCollapse"
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
      </el-aside>
      </el-container>
      <el-container class="header2">
        <div class="search-box">
          <form class="inline" onsubmit="return false;">
            <input v-model="search" type="text" class="input" placeholder="搜一下就知道！" @keydown.enter="Search" >
            <el-button class="button" @click="Search">
              <span class="text">Search</span>
            </el-button>
            <el-button v-if="filter===false & shouldShow===true" class="button" @click="changeStyle1">
              <span class="text">筛选</span>
            </el-button>
            <el-button v-if="filter===true & shouldShow===true" class="button" @click="changeStyle2">
              <span class="text">收起</span>
            </el-button>
            <el-button v-if="shouldShow===false" class="button" @click="open_compare=true">
              <span class="text">比价</span>
            </el-button>
          </form>
          <el-menu
              default-active="1"
              class="el-menu-demo"
              mode="horizontal"
          >
            <el-menu-item  @click="model=1" index="1" class="icon1">
              <p class="text">京东</p>
            </el-menu-item>
            <el-menu-item @click="model=2" index="2" class="icon1">
              <p class="text">苏宁</p>
            </el-menu-item>
            <el-menu-item @click="model=3" index="3" class="icon1">
              <p class="text">唯品会</p>
            </el-menu-item>
          </el-menu>
        </div>
        <div v-if="filter===true" class="filter">
          <div class="Compare">
            <div v-if="Object.keys(fork_JD_good).length > 0" class="compare">
              <p class="card_font">{{fork_JD_good.title}}</p>
              <p class="card_price">￥{{fork_JD_good.price}}</p>
              <el-button class="button filter_button" @click="fork_JD_good={}">
                <span class="text filter_text">清除</span>
                <span class="text filter_text" style="color: brown">京东</span>
              </el-button>
            </div>
            <div v-else-if="Object.keys(fork_JD_good).length === 0" class="compare">
              <p class="no_goods">请添加</p>
              <span class="no_goods" style="color: brown">京东</span>
              <p class="no_goods">商品</p>
            </div>
            <div v-if="Object.keys(fork_SN_good).length > 0" class="compare">
              <p class="card_font">{{fork_SN_good.title}}</p>
              <p class="card_price">￥{{fork_SN_good.price}}</p>
              <el-button class="button filter_button" @click="fork_SN_good={}">
                <span class="text filter_text">清除</span>
                <span class="text filter_text" style="color: #edd55c">苏宁</span>
              </el-button>
            </div>
            <div v-else-if="Object.keys(fork_SN_good).length === 0" class="compare">
              <p class="no_goods">请添加</p>
              <span class="no_goods" style="color: #edd55c">苏宁</span>
              <p class="no_goods">商品</p>
            </div>
            <div v-if="Object.keys(fork_A_good).length > 0" class="compare">
              <p class="card_font">{{fork_A_good.title}}</p>
              <p class="card_price">￥{{fork_A_good.price}}</p>
              <el-button class="button filter_button" @click="fork_A_good={}">
                <span class="text filter_text">清除</span>
                <span class="text filter_text" style="color: #e145df">唯品会</span>
              </el-button>
            </div>
            <div v-else-if="Object.keys(fork_A_good).length === 0" class="compare">
              <p class="no_goods">请添加</p>
              <span class="no_goods" style="color: #e145df">唯品会</span>
              <p class="no_goods">商品</p>
            </div>
          </div>
          <div class="filter_area">
            <input v-model="this.filter_search" class="input filter_input" placeholder="筛选"/>
            <br/><br/>
            <el-button class="button " @click="sortProducts">
              <span class="text">按价格排序</span>
            </el-button>
            <el-button class="button " @click="open_compare=true">
              <span class="text">详细价格比较</span>
            </el-button>
          </div>
        </div>
      </el-container>
      <el-main :class="mainClass" v-loading.body.lock="load">
        <div v-if="model===1" class="commodity">
            <div v-if="JD_search_goods.length>0" class="JD" v-for="good in JD_search_goods">
              <el-card class="good_card">
                <div class="card_body">
                  <img class="image" :src="good.img" :alt="good.id">
                  <p class="card_font">{{good.title}}</p>
                  <p class="card_price">￥{{good.price}}</p>
                  <p class="card_font card_shop_font">{{good.shop}}</p>
                </div>
                <template #footer >
                  <div class="card_footer">
                    <el-button  class="card_button" @click="JD_fork(good)">
                      <span class="text card_text ">固定</span>
                    </el-button>
                    <el-button  class="card_button" @click="add_car_JD(good)" >
                      <span class="text card_text_icon"><el-icon><ShoppingCartFull /></el-icon></span>
                    </el-button>
                    <el-button  class="card_button" @click="openLink(good.link)">
                      <span class="text card_text" >详情</span>
                    </el-button>
                  </div>
                </template>
              </el-card>
            </div>
            <div v-else class="center">
              <el-empty class="text1" description="搜索界面空空......" />
            </div>
        </div>
        <div v-if="model===2" class="commodity">
          <div  v-if="SN_search_goods.length>0" class="JD" v-for="good in SN_search_goods">
            <el-card class="good_card">
              <div class="card_body">
                <img class="image" :src="good.img" :alt="good.id">
                <p class="card_font">{{good.title}}</p>
                <p class="card_price">￥{{good.price}}</p>
                <p class="card_font card_shop_font">{{good.shop}}</p>
              </div>
              <template #footer >
                <div class="card_footer">
                  <el-button  class="card_button" @click="SN_fork(good)">
                    <span class="text card_text ">固定</span>
                  </el-button>
                  <el-button  class="card_button" @click="add_car_SN(good)">
                    <span class="text card_text_icon"><el-icon><ShoppingCartFull /></el-icon></span>
                  </el-button>
                  <el-button  class="card_button" @click="openLink(good.link)">
                    <span class="text card_text" >详情</span>
                  </el-button>
                </div>
              </template>
            </el-card>
          </div>
          <div v-else class="center">
            <el-empty class="text1" description="搜索界面空空......" />
          </div>
        </div>
        <div v-if="model===3" class="commodity">
          <div  v-if="A_search_goods.length>0" class="JD" v-for="good in A_search_goods">
            <el-card class="good_card">
              <div class="card_body">
                <img class="image" :src="good.img" :alt="good.id">
                <p class="card_font">{{good.title}}</p>
                <p class="card_price">￥{{good.price}}</p>
                <p class="card_font card_shop_font">{{good.shop}}</p>
              </div>
              <template #footer >
                <div class="card_footer">
                  <el-button  class="card_button" @click="A_fork(good)">
                    <span class="text card_text ">固定</span>
                  </el-button>
                  <el-button  class="card_button" @click="add_car_A(good)">
                    <span class="text card_text_icon"><el-icon><ShoppingCartFull /></el-icon></span>
                  </el-button>
                  <el-button  class="card_button" @click="openLink(good.link)" >
                    <span class="text card_text" >详情</span>
                  </el-button>
                </div>
              </template>
            </el-card>
          </div>
          <div v-else class="center">
            <el-empty  class="text1" description="搜索界面空空......" />
          </div>
        </div>
      </el-main>
      <el-container v-if="!shouldShow" class="bottom">
        <el-menu
            default-active="1"
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

  <el-dialog
      v-model="open_compare"
      :style="{ width: shouldShow ? '70%' : '100%' }"
  >
    <template #header>
      <span class="dia_font">详细比价</span>
    </template>
    <div class="dialog_body" v-if="shouldShow">
      <div  class="JD" >
        <el-card class="good_card">
          <div v-if="Object.keys(fork_JD_good).length > 0" >
            <img class="image" :src="fork_JD_good.img" :alt="fork_JD_good.id">
            <p class="card_font">{{fork_JD_good.title}}</p>
            <p class="card_price">￥{{fork_JD_good.price}}</p>
            <p class="card_font card_shop_font">店铺：{{fork_JD_good.shop}}</p>
            <p class="card_font card_shop_font">销量：{{fork_JD_good.sales}}</p>
            <el-button  class="card_button" @click="add_car_JD(this.fork_JD_good)">
              <span class="text card_text_icon"><el-icon><ShoppingCartFull /></el-icon></span>
            </el-button>
            <el-button  class="card_button"  @click="openLink(fork_JD_good.link)">
              <span class="text card_text" >详情</span>
            </el-button>
            <el-button class="card_button" @click="fork_JD_good={}">
              <span class="text filter_text">清除</span>
              <span class="text filter_text" style="color: brown">京东</span>
            </el-button>
          </div>
          <div v-else class="dia_compare">
            <p class="no_goods">请添加</p>
            <span class="no_goods" style="color: brown">京东</span>
            <p class="no_goods">商品</p>
          </div>
        </el-card>
      </div>
      <div  class="JD" >
        <el-card class="good_card">
          <div  v-if="Object.keys(fork_SN_good).length > 0">
            <img class="image" :src="fork_SN_good.img" :alt="fork_SN_good.id">
            <p class="card_font">{{fork_SN_good.title}}</p>
            <p class="card_price">￥{{fork_SN_good.price}}</p>
            <p class="card_font card_shop_font">{{fork_SN_good.shop}}</p>
            <el-button  class="card_button" >
              <span class="text card_text_icon"><el-icon><ShoppingCartFull /></el-icon></span>
            </el-button>
            <el-button  class="card_button" @click="openLink(fork_SN_good.link)">
              <span class="text card_text" >详情</span>
            </el-button>
            <el-button class="card_button" @click="fork_SN_good={}">
              <span class="text filter_text">清除</span>
              <span class="text filter_text" style="color: #edd55c">苏宁</span>
            </el-button>
          </div>
          <div v-else class="dia_compare">
            <p class="no_goods">请添加</p>
            <span class="no_goods" style="color: #edd55c">苏宁</span>
            <p class="no_goods">商品</p>
          </div>
        </el-card>
      </div>
      <div  class="JD" >
        <el-card class="good_card">
          <div v-if="Object.keys(fork_A_good).length > 0" >
            <img class="image" :src="fork_A_good.img" :alt="fork_A_good.id">
            <p class="card_font">{{fork_A_good.title}}</p>
            <p class="card_price">￥{{fork_A_good.price}}</p>
            <p class="card_font card_shop_font">{{fork_A_good.shop}}</p>
            <el-button  class="card_button" >
              <span class="text card_text_icon"><el-icon><ShoppingCartFull /></el-icon></span>
            </el-button>
            <el-button  class="card_button"  @click="openLink(fork_A_good.link)">
              <span class="text card_text" >详情</span>
            </el-button>
            <el-button class="card_button" @click="fork_A_good={}">
              <span class="text filter_text">清除</span>
              <span class="text filter_text" style="color: #e145df">唯品会</span>
            </el-button>
          </div>
          <div v-else class="dia_compare">
            <p class="no_goods">请添加</p>
            <span class="no_goods" style="color: #e145df">唯品会</span>
            <p class="no_goods">商品</p>
          </div>
        </el-card>
      </div>
    </div>
    <div class="Compare" v-else>
      <div v-if="Object.keys(fork_JD_good).length > 0" class="compare">
        <p class="card_font">{{fork_JD_good.title}}</p>
        <p class="card_price">￥{{fork_JD_good.price}}</p>
        <el-button class="button filter_button" @click="fork_JD_good={}">
          <span class="text filter_text">清除</span>
          <span class="text filter_text" style="color: brown">京东</span>
        </el-button>
      </div>
      <div v-else-if="Object.keys(fork_JD_good).length === 0" class="compare">
        <p class="no_goods">请添加</p>
        <span class="no_goods" style="color: brown">京东</span>
        <p class="no_goods">商品</p>
      </div>
      <div v-if="Object.keys(fork_SN_good).length > 0" class="compare">
        <p class="card_font">{{fork_SN_good.title}}</p>
        <p class="card_price">￥{{fork_SN_good.price}}</p>
        <el-button class="button filter_button" @click="fork_SN_good={}">
          <span class="text filter_text">清除</span>
          <span class="text filter_text" style="color: #edd55c">苏宁</span>
        </el-button>
      </div>
      <div v-else-if="Object.keys(fork_SN_good).length === 0" class="compare">
        <p class="no_goods">请添加</p>
        <span class="no_goods" style="color: #edd55c">苏宁</span>
        <p class="no_goods">商品</p>
      </div>
      <div v-if="Object.keys(fork_A_good).length > 0" class="compare">
        <p class="card_font">{{fork_A_good.title}}</p>
        <p class="card_price">￥{{fork_A_good.price}}</p>
        <el-button class="button filter_button" @click="fork_A_good={}">
          <span class="text filter_text">清除</span>
          <span class="text filter_text" style="color: #e145df">唯品会</span>
        </el-button>
      </div>
      <div v-else-if="Object.keys(fork_A_good).length === 0" class="compare">
        <p class="no_goods">请添加</p>
        <span class="no_goods" style="color: #e145df">唯品会</span>
        <p class="no_goods">商品</p>
      </div>
    </div >
    <template #footer>
      <el-button class="button dia_button" @click="open_compare = false">
        <span class="text">关闭</span>
      </el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet');
.center{
  margin-left: 600px;
}
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
  height: 18%;
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
  z-index:10
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
  top: 28vh;
  left: 4vw;
  width: 96%;
  height: 72%;
  background-image: url("./icons/layered-waves-haikei.svg");
  background-repeat: no-repeat;
  background-position: right bottom;
  background-size: cover;
}
.new-top {
  top: 48vh !important;
  height: 52% !important;
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
  font-family: 'Montserrat', sans-serif;
  font-size:2vh;
  font-weight: 600;
  text-transform: uppercase;
}
.commodity{
  display: flex;
  flex-wrap: wrap;
  justify-content: start;
  margin-left: 100px;
}
.good_card{
  width: 100%;
  height: 100%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease, transform 0.3s ease;
  background-image: url("./icons/polygon-scatter-haikei.svg");
}
.good_card:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
}
.header2{
  position: absolute;
  top: 8vh;
  width: 96%;
  height: 18%;
}
.filter{
  position: absolute;
  top: 18vh;
  left: 4vw;
  width: 90%;
  height: 20vh;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.JD{
  width: 320px;
  height: 500px;
  margin: 10px;
}
.card_body{
  height:400px;
  background-color: rgba(255, 255, 255, 0.41);
}
.card_font{
  font-family: 'Montserrat', sans-serif;
  color: #000000;
  font-size: 13px;
  font-style: italic;
  font-weight: 600;
  letter-spacing: 1px;
}
.image{
  height: 50%;
  width: 80%;
  margin: 10%;
}
.card_price{
  margin-top: 10px;
  font-family: 'Montserrat', sans-serif;
  color: #f11c1c;
  font-size: 17px;
  font-style: italic;
  font-weight: 600;
  letter-spacing: 2px;
}
.card_footer{
  height: 90px !important;
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  justify-content: start;
}
.card_button {
  background-color: #0b59cf;
  margin-left: 1%;
  padding: 2.5% 0.5%;
  width: 80px;
  border-radius: 10px;
  border: 2px solid #0b59cf;
  box-shadow: 0 4px 16px rgb(10, 64, 165,0.2);
  transition: .2s;
  color: #f5f7f8;
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
.card_text{
  font-size: 14px;
}
.card_text_icon{
  font-size: 22px;
}
.card_shop_font{
  font-size: 10px;
  font-weight: 300;
}
.el-menu-demo{
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  height: 8vh;
}
.Compare{
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  width: 70%;
  height: 100%;
}
.compare{
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  width: 30%;
  margin: 10px;
  height: 90%;
  border: 2px solid #000;
}
.no_goods{
  font-family: 'Montserrat', sans-serif;
  color: #000000;
  font-size: 100%;
  font-style: italic;
  font-weight: 900;
  letter-spacing: 2px;
  margin-bottom: 1%;
}
.filter_area{
  width: 30%;
  height: 100%;
}
.filter_button{
  width: 60px !important;
}
.filter_text{
  font-size: 11px !important;
  font-weight:bold !important;
}
.filter_input{
  margin-top: 10px;
  width: 70%!important;
}
.dia_font{
  font-family: 'Montserrat', sans-serif;
  font-style: italic;
  font-weight: 600;
  letter-spacing: 2px;
  color: #0b59cf;
  font-size: 30px;
  display: flex;
  justify-content: center;
}
.dia_button{
  width: 90px;
  height: 10px!important;
}
.dialog_body{
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  width: 100%;
}
.dia_compare{
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 80%;
  font-size: 20px !important;
}
@media (max-width: 500px) {
  .center{
    margin-left: 80px;
  }
  .main{
    position: absolute;
    top: 24vh;
    left: 0;
    width: 100%;
    height:68vh;
  }
  .new-top {
    position: absolute;
    top: 15vh !important;
    left: 12vw !important;
    width: 88% !important;
    height:85% !important;
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
  .search-box{
    position: absolute;
    margin-left: 10vw;
    margin-top: 3%;
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
    padding: 2.5% 4%;
    width: 55px;
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
    box-shadow: 0 2px 2px rgba(40, 97, 191, 0.6);
    border-width: 2px;
  }
  .text{
    font-size:12px;
    font-weight: 600;
    text-transform: uppercase;
  }
  .JD{
    width: 74%;
    height: 350px;
    margin-left: 13%;
  }
  .commodity{
     display: flex;
     flex-wrap: wrap;
     justify-content: start;
     margin-left: 0;
   }
  .good_card{
    width: 100%;
    height: 100%;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s ease, transform 0.3s ease;
  }
  .good_card:hover {
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
    transform: translateY(-2px);
  }
  .card_body{
    height:260px;
  }
  .card_font{
    font-family: 'Montserrat', sans-serif;
    color: #000000;
    font-size: 11px;
    font-style: italic;
    font-weight: 700;
    letter-spacing: 0;
  }
  .image{
    height: 150px;
    width: 150px;
    margin-left: 30px;
    margin-top: 5px;
  }
  .card_price{
    margin-top: 1px;
    font-family: 'Montserrat', sans-serif;
    color: #f11c1c;
    font-size: 14px;
    font-style: italic;
    font-weight: 600;
    letter-spacing: 1px;
  }
  .card_footer{
    width: 100% !important;
    margin-top: -10px;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }
  .card_button {
    background-color: #0b59cf;
    width: 50px;
    margin-left: 0;
    margin-right: 0;
    border-radius: 8px;
    border: 1px solid #0b59cf;
    box-shadow: 0 2px 10px rgb(10, 64, 165,0.2);
    transition: .2s;
    color: #f5f7f8;
  }
  .card_text{
    font-size: 13px;
  }
  .card_text_icon{
    font-size: 20px;
  }
  .card_shop_font{
    font-size: 8px;
    font-weight: 400;
  }
  .el-menu-demo{
    margin-left: 5px;
    margin-top: 10px;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    height: 8vh;
    width: 300px;
  }
  .icon1{
    margin-left: 0;
  }
  .Compare{
    width: 100%;
    height: 380px;
  }
  .compare{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    width: 80%;
    margin: 3px;
    height: 120px;
    border: 2px solid #000;
    font-size: 11px !important;
  }
}
</style>