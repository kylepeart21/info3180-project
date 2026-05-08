import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'
import LogoutView from '../views/LogoutView.vue'
import NewProfileView from '../views/NewProfileView.vue'
import ProfileDetailsView from '../views/ProfileDetailsView.vue'
import FavouritesView from '../views/FavouritesView.vue'
import UserProfileView from "../views/UserProfileView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/logout',
      name: 'logout',
      component: LogoutView
    },
    {
      path: '/users/:user_id',
      name: 'User Profile',
      component: UserProfileView
    },
    {
      path: '/profiles/new',
      name: 'New Profile',
      component: NewProfileView
    },
    {
      path: '/profiles/favourites',
      name: 'Show User Favourites',
      component: FavouritesView
    },
    {
      path: '/profiles/:profile_id',
      name: 'Profile Details',
      component: ProfileDetailsView
    }
  ]
})

export default router
