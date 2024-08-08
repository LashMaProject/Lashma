import { createStore } from 'vuex';

export default createStore({
  state: {
    user: null,
    accessToken: null,
    refreshToken: null,
  },
  mutations: {
    SET_USER(state, payload) {
      state.user = payload.username;
      state.accessToken = payload.access_token;
      state.refreshToken = payload.refresh_token;
    },
    LOGOUT(state) {
      state.user = null;
      state.accessToken = null;
      state.refreshToken = null;
      localStorage.removeItem('refresh_token');
    },
  },
  actions: {
    async refreshToken({ commit }) {
    // Send a refresh token request to your backend
    // ... handle response and update tokens in the store
    try {
      const response = await axios.post('/api/refresh-token');
      const { access_token, refresh_token } = response.data;
      commit('SET_USER', { access_token, refresh_token });
    } catch (error) {
      console.error('Failed to refresh token:', error);
      // Handle error, e.g. redirect to login page
    }
    },
  },
});
