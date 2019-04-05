import Vue from 'vue';
import Router from 'vue-router';
import Ping from '@/components/Ping';
import Shows from '@/components/Shows';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Shows',
      component: Shows,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
  mode: 'hash',
});
