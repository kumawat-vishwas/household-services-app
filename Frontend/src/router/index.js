import { createRouter, createWebHistory } from 'vue-router';

import NotFound from '../components/not_found.vue'; 
import IndexPage from '../components/IndexPage.vue';
import userProfile from '../components/user_profile.vue';
import userSummary from '../components/user_summary.vue';
import professionalSummary from '../components/professional_summary.vue';
import adminDashboard from '../components/admin_dashboard.vue';
import adminSummary from '../components/admin_summary.vue';
import professionalProfile from '../components/professional_profile.vue';
import blocked from '../components/blocked.vue';
import logout from '../components/logout.vue';
import userDashboard from '../components/user_dashboard.vue'; 
import professionalDashboard from '../components/professional_dashboard.vue';  




import store from '@/store'; 

const routes = [
  {
    path: '/',
    name: 'IndexPage',
    component: IndexPage,
  },
  {
    path: '/user/dashboard',
    name: 'userDashboard',
    component: userDashboard,
    meta: { requiresAuth: true, showNavbarUser: true },
  },
  {
    path: '/user/profile',
    name: 'userProfile',
    component: userProfile,
    meta: { requiresAuth: true, showNavbarUser: true },
  },
  {
    path: '/user/summary',
    name: 'userSummary',
    component: userSummary,
    meta: { requiresAuth: true, showNavbarUser: true },
  },
  {
    path: '/service-professional/dashboard',
    name: 'professionalDashboard',
    component: professionalDashboard,
    meta: { requiresAuth: true, showNavbarServiceProfessional: true },
  },
  {
    path: '/service-professional/summary',
    name: 'professionalSummary',
    component: professionalSummary,
    meta: { requiresAuth: true, showNavbarServiceProfessional: true },
  },
  {
    path: '/service-professional/profile',
    name: 'professionalProfile',
    component: professionalProfile,
    meta: { requiresAuth: true, showNavbarServiceProfessional: true },
  },
  {
    path: '/admin/dashboard',
    name: 'adminDashboard',
    component: adminDashboard,
    meta: { requiresAuth: true, showNavbarAdmin: true },
  },
  {
    path: '/admin/summary',
    name: 'adminSummary',
    component: adminSummary,
    meta: { requiresAuth: true, showNavbarAdmin: true },
  },
  {
    path: '/blocked',
    name: 'blocked',
    component: blocked,
    meta: { requiresAuth: true},
  },

  {
    path: '/logout',
    name: 'logout',
    component: logout,
  },
  {
    path: '/:catchAll(.*)',
    component: NotFound, 
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !store.getters.isAuthenticated ) {
    next({ path: 'logout' }); 
  } else {
    next(); 
  }
});

export default router;