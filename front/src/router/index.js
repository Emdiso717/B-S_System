import { createRouter, createWebHistory } from 'vue-router'
import LoginVue from '@/components/login.vue'
import MainVue from  '@/components/main.vue'
import CarVue from  '@/components/car.vue'
import UserVue from  '@/components/user.vue'
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
        }
    ]

})
export default router