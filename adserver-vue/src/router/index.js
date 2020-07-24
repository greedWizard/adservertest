import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import Login from '@/components/Login'
import Registration from '@/components/users/Registration'
import Profile from '@/components/users/Profile'
import CreateAd from '@/components/board/CreateAd'
import AdDetails from '@/components/board/AdDetails'
import AdsByUser from '@/components/board/AdsByUser'
import EditAd from '@/components/board/EditAd'
import DeleteAd from '@/components/board/DeleteAd'
import MyDialogues from '@/components/chat/MyDialogues'
import Dialogue from '@/components/chat/Dialogue'
import Search from '@/components/board/Search'

Vue.use(Router)

export default new Router({
  routes: [
    // Пользователи
    {
      path: '/',
      name: 'index',
      component: Index
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/register',
      name: 'registration',
      component: Registration
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
    },
    // Доска/Объявления
    {
      path: '/new_add',
      name: 'createAd',
      component: CreateAd,
    },
    {
      path: '/ad/id:ad_id',
      name: 'adDetails',
      component: AdDetails,
    },
    {
      path: '/ads/by_user/id:user_id',
      name: 'adsByUser',
      component: AdsByUser,
    },
    {
      path: '/ad/id:ad_id/edit',
      name: 'editAd',
      component: EditAd,
    },
    {
      path: '/ad/id:ad_id/delete',
      name: 'deleteAd',
      component: DeleteAd,
    },
    // Чат
    {
      path: '/chat/my_dialogues',
      name: 'myDialogues',
      component: MyDialogues,
    },
    {
      path: '/chat/dialogue/:dialogue_id',
      name: 'dialogue',
      component: Dialogue,
    },
    // Поиск
    {
      path: '/board/search',
      name: 'search',
      component: Search,
    }
  ]
})
