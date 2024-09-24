import { createRouter, createWebHistory } from 'vue-router'
import LoginVue from '@/components/login.vue'

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
        }
    ]

})
export default router