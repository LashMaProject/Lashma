import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios';
import Toast from 'vue-toastification'

// Set the base URL for API requests
axios.defaults.baseURL = 'http://localhost:5000';
//create app with router and toast
createApp(App).use(router).use(store).use(Toast).mount('#app');
