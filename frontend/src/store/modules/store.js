/* eslint-disable no-undef */
/* eslint-disable no-unused-vars */
import { createStore } from 'vuex';
import auth from './modules/auth/index';


const store = createStore({
    modules: {
        auth,
    }
});