/* eslint-disable no-undef */
/* eslint-disable no-unused-vars */
import { get } from "core-js/core/dict";
import mutations from "./mutations";
import actions from "./actions";
import getters from "./getters";

export default {
    namespaced: true,
    state() {
        return {
            name: 'State Leela',
        }
    },
    mutations,
    actions,
    getters,
};