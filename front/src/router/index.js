import { createRouter, createWebHistory } from 'vue-router'
import LoginVue from '@/components/login.vue'
import MainVue from  '@/components/main.vue'
import CarVue from  '@/components/car.vue'
import UserVue from  '@/components/user.vue'
import AVue from '@/components/login_A.vue'
import SNVue from '@/components/login_SN.vue'
import JDVue from '@/components/login_JD.vue'
import adminVue from '@/components/admin.vue'
import { jwtDecode } from 'jwt-decode';
import {ElMessage} from "element-plus";
const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes:[
        {
            path: '/',
            redirect: '/login'
        },
        {
            path:'/login',
            component : LoginVue
        },
        {
            path:'/main',
            name:'Main',
            component : MainVue,
            props: true
        },
        {
            path:'/car',
            name:'Car',
            component : CarVue,
            props: true
        },
        {
            path:'/user',
            name:'User',
            component : UserVue,
            props: true
        },
        {
            path:'/wph',
            name:'A',
            component : AVue,
            props: true
        },
        {
            path:'/SN',
            name:'SN',
            component : SNVue,
            props: true
        },
        {
            path:'/JD',
            name:'JD',
            component : JDVue,
            props: true
        },
        {
            path:'/admin',
            name:'admin',
            component : adminVue,
            props: true
        },
    ]

});
function getToken(username) {
    return localStorage.getItem(`authToken_${username}`);
}
function isTokenExpired(token) {
    try {
        const decodedToken = jwtDecode(token);
        const expirationTime = decodedToken.exp * 1000; // JWT中的exp是以秒为单位的，需要转换为毫秒
        const currentTime = new Date().getTime();
        return currentTime >= expirationTime;
    } catch (error) {
        console.error('Failed to decode token:', error);
        return true; // 如果Token解码失败，则认为Token无效
    }
}
router.beforeEach((to, from, next) => {
    if (to.path === '/login') {
        next();
    }
    else{
        if (to.query.account) {
            console.log('Account:', to.query.account);
            const token = getToken(to.query.account);
            if(!token){
                next('/login');
            }
            else
            {
                if(!isTokenExpired(token)){
                    next();
                }else{
                    next('/login');
                    localStorage.removeItem(`authToken_${to.query.account}`);
                    ElMessage.error("登录过期，请重新登录！")
                }
            }
        }else{
            next('/login');
        }
    }


});


export default router