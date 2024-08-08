<template>
  <form @submit.prevent="login">
    <div class="form-group">
      <label for="username">Username:</label>
      <input type="text" id="username" v-model="username" required />
    </div>
    <div class="form-group">
      <label for="password">Password:</label>
      <input type="password" id="password" v-model="password" required />
    </div>
    <div class="form-group">
      <input type="checkbox" id="rememberMe" v-model="rememberMe" />
      <label for="rememberMe">Remember Me</label>
    </div>
    <button type="submit">Login</button>
    <p v-if="error">{{ error }}</p>
  </form>
</template>

<script>
import { ref } from "vue";
import { useStore } from "vuex";
import axios from "axios";

export default {
  setup() {
    const store = useStore();
    const username = ref("");
    const password = ref("");
    const rememberMe = ref(false);
    const error = ref(null);

    const login = async () => {
      try {
        const response = await axios.post("/login", {
          username: username.value,
          password: password.value,
        });
        const { access_token, refresh_token } = response.data;

        store.commit("SET_USER", {
          username: username.value,
          access_token,
          refresh_token,
        });

        if (rememberMe.value) {
          localStorage.setItem("refresh_token", refresh_token); // Or use cookies
        }

        // Redirect to the main page
      } catch (err) {
        error.value = err.response.data.msg || "Error logging in";
      }
    };

    return { username, password, rememberMe, error, login };
  },
};
</script>
