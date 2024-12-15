<script>
import {Document, HomeFilled, Setting, ShoppingCartFull, User, UserFilled} from "@element-plus/icons-vue";
import {ElMessage} from "element-plus";
import axios from "axios";
import * as echarts from "echarts";
import {nextTick, ref} from "vue";

export default {
  components: { User, ShoppingCartFull, UserFilled, HomeFilled, Setting, Document},
  data(){
    return{
      shouldShow: true,
      account:'',
      isCollapse:true,
      car:[],
      price:false,
      myChart: {},
      xData: [1,2,3,4,5],
      yData: [],
      myChartStyle: { float: "left", width: "500px", height: "400px" } //图表样式
    }
  },
  created() {
    this.account = this.$route.query.account;
    console.log('Received account:', this.account);
  },
  mounted() {
    this.search_car();
    this.checkWidth();
    window.addEventListener('resize', this.checkWidth);
  },
  methods: {
    checkWidth() {
      this.shouldShow = window.innerWidth >= 500;
    },
    open(good){
      this.price = true;
      this.yData=[];
      this.yData.push(good.price1)
      this.yData.push(good.price2)
      this.yData.push(good.price3)
      this.yData.push(good.price4)
      this.yData.push(good.price)
      nextTick(() => {
        this.initEcharts();
      });
    },
    initEcharts() {
      const option = {
        xAxis: {
          data: this.xData
        },
        yAxis: {},
        series: [
          {
            data: this.yData,
            type: "line",
            label: {
              show: true,
              position: "top",
              textStyle: {
                fontSize: 16
              }
            }
          }
        ]
      };
      this.myChart = echarts.init(document.getElementById("chart"));
      this.myChart.setOption(option);
    },
    changeRoute(path) {
      const currentRoute = this.$route;
      this.$router.push({
        path: path,
        query: currentRoute.query
      });
    },
    search_car(){
      axios.post("/scar",
          {
            account:this.account,
          }).then(response => {
        let message = response.data
        if(message.length ===0){
          this.car=[]
          // ElMessage.error("没有结果")
        }else {
          this.car=message
        }
      })
    },
    openLink(link){
      window.open(link);
    },
    delete_car(good){
      axios.post("/delete",
          {
            account:this.account,
            good_id:good.id
          }).then(response => {
        let message = response.data
        if(message.includes("success")){
          ElMessage.success("删除成功")
        }else {
          ElMessage.error("删除失败")
        }
        this.search_car();
      })
    },
    backgroundClass(good){
        if(good.from ==='京东')
          return 'background_img1';
        else if(good.from === '苏宁')
          return 'background_img2';
        else
          return 'background_img3';
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
      <div  class="commodity" v-if="this.car.length > 0" >
        <div  class="JD" v-for="good in car">
          <el-card class="good_card" :class="backgroundClass(good)">
            <div class="card_body">
              <img class="image" :src="good.img" :alt="good.id">
              <p class="card_font">{{good.title}}</p>
              <p class="card_price" v-if="good.price > 0">
                ￥{{ good.price }}
              </p>
              <p class="card_price" v-else>
                无货或已下架
              </p>
              <p class="card_font card_shop_font">{{good.from}}</p>
            </div>
            <template #footer >
              <div class="card_footer">
                <el-popconfirm width="220" title="请确认删除" class="text" @confirm="delete_car(good)">
                  <template #reference>
                    <el-button  class="card_button button_delete" >
                      <span class="text card_text">从购物车删除</span>
                    </el-button>
                  </template>
                  <template #actions="{cancel,confirm}">
                    <el-button size="small" @click="cancel">No</el-button>
                    <el-button type="danger" size="small"   @click="confirm">Yes</el-button>
                  </template>
                </el-popconfirm>
                <el-button  class="card_button" @click="openLink(good.link)">
                  <span class="text card_text" >详情</span>
                </el-button>
                <el-button  class="card_button" @click="open(good)">
                  <span class="text card_text" >价格走势</span>
                </el-button>
              </div>
            </template>
          </el-card>
        </div>
      </div>
      <div v-else class="center">
        <el-empty class="text1" description="购物车空空哦......" />
      </div>
    </el-main>
    <el-container v-if="!shouldShow" class="bottom">
      <el-menu
          default-active="2"
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


  <el-dialog v-if="shouldShow" v-model="price" width="50%">
    <template #header>
      <span class="dia_font">详细比价</span>
    </template>
    <div class="dialog_body" >
      <div id="chart" :style="myChartStyle"></div>
    </div>
    <template #footer>
      <el-button class="dia_button" @click="price=false">
        <span class="text">关闭</span>
      </el-button>
    </template>
  </el-dialog>

  <el-dialog v-if="!shouldShow" v-model="price" width="90%">
    <template #header>
      <span class="dia_font">详细比价</span>
    </template>
    <div class="dialog_body" >
      <div id="chart" :style="myChartStyle"></div>
    </div>
    <template #footer>
      <el-button class="dia_button" @click="price=false">
        <span class="text">关闭</span>
      </el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet');
.text{
  font-size:12px;
  font-weight: 600;
  text-transform: uppercase;
}
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
  background-image: url("./icons/layered-peaks-haikei.svg");
  background-repeat: no-repeat;
  background-position: right bottom;
  background-size: cover;
}
.JD{
  width: 320px;
  height: 500px;
  margin: 10px;

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
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}
.background_img1{
  background-image:url('./icons/circle-scatter-haikei_JD.svg');
  background-position: right bottom;
}
.background_img2{
  background-image:url('./icons/circle-scatter-haikei_SN.svg');
  background-position: right bottom;

}
.background_img3{
  background-image:url('./icons/circle-scatter-haikei_A.svg');
  background-position: right bottom;

}
.background{
  position: absolute;
  width: 320px;
  height: 440px;
  margin-left: -20px;
  margin-top: -20px;
  z-index: 0;
  overflow: hidden;
}
.good_card:hover {
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4);
  transform: translateY(-2px);
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
  position: relative;
  z-index: 1;
  height: 90px !important;
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.card_button {
  background-color: #0b59cf;
  margin-left: 0;
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
.button_delete{
  width: 85px !important;
  background-color: #cf0b46 !important;
  border: 2px solid #cf0b46 !important;
  box-shadow: 0 4px 16px rgb(103, 10, 39) !important;
  color: #f5f7f8!important;
}
.button_delete:hover {
  background-color: #ffffff!important;
  color: #cf1121 !important;
  border-color: #cf0b46 !important;
  box-shadow: 0 4px 16px rgb(103, 10, 39) !important;
}
.card_text{
  font-size: 14px;
}
.card_shop_font{
  font-size: 10px;
  font-weight: 300;
}
.card_body{
  position: relative;
  z-index: 1;
  height:400px;
  background-color: rgba(255, 255, 255, 0.41);
}
.center{
  display: flex;
  justify-content: center;
  align-items: center;
}
.text1{
  margin-top: 13%;

}
.dia_button{
  background-color: #0b59cf;
  margin-left: 0;
  padding: 1% 0.5%;
  width: 60px;
  border-radius: 10px;
  border: 2px solid #0b59cf;
  box-shadow: 0 4px 16px rgb(10, 64, 165,0.2);
  transition: .2s;
  color: #f5f7f8;
}
.dia_button:active,
.dia_button:focus,
.dia_button:hover {
  background-color: #ffffff;
  transition: box-shadow 0.3s ease;
  color: #2f4a78;
  border-color: #2861bf;
  box-shadow: 0 4px 16px rgba(40, 97, 191, 0.6);
  border-width: 3px;
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
.dialog_body{
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  width: 100%;
}
.shape{
  transform: rotate(45deg);
  position: absolute;
  opacity:0.2;
  height: 500px;
  width: 80px;
  top: 100px;
  right: 10px;
  z-index: 1;
  border-radius:  30px ;
  box-shadow: 10px 10px 5px rgba(117, 35, 35, 0.3);
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
    margin-left: 0;
  }
  .card_button {
    background-color: #0b59cf;
    width: 50px;
    margin-left: -10px;
    margin-right: 0;
    border-radius: 8px;
    border: 1px solid #0b59cf;
    box-shadow: 0 2px 10px rgb(10, 64, 165,0.2);
    transition: .2s;
    color: #f5f7f8;
  }
  .card_text{
    font-size: 12px;
  }
  .card_shop_font{
    font-size: 8px;
    font-weight: 400;
  }
  .JD{
    width: 76%;
    height: 350px;
    margin-left: 12%;
  }
  .commodity{
    display: flex;
    flex-wrap: wrap;
    justify-content: start;
    margin-left: 0;
  }
  .icon{
    margin-left: 13% !important;
  }
  .button_delete{
    width: 85px !important;
    background-color: #cf0b46 !important;
    border: 2px solid #cf0b46 !important;
    box-shadow: 0 4px 16px rgb(103, 10, 39) !important;
    color: #f5f7f8!important;
  }
  .button_delete:hover {
    background-color: #ffffff!important;
    color: #cf1121 !important;
    border-color: #cf0b46 !important;
    box-shadow: 0 4px 16px rgb(103, 10, 39) !important;
  }
}
</style>