<template>
  <form @submit.prevent="register">
    <div class="form-group">
      <label for="username">Username:</label>
      <input type="text" id="username" v-model="username" required />
      <div v-if="errors.username" class="error">{{ errors.username[0] }}</div>
    </div>
    <div class="form-group">
      <label for="email">Email:</label>
      <input type="email" id="email" v-model="email" required />
      <div v-if="errors.email" class="error">{{ errors.email[0] }}</div>
    </div>
    <div class="form-group">
      <label for="password">Password:</label>
      <input type="password" id="password" v-model="password" required />
      <div v-if="errors.password" class="error">{{ errors.password[0] }}</div>
    </div>
    <button type="submit">Register</button>
    <p v-if="successMessage">{{ successMessage }}</p>
  </form>
</template>

<script>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

export default {
  setup() {
    const username = ref("");
    const email = ref("");
    const password = ref("");
    const errors = ref({});
    const successMessage = ref(null);
    const router = useRouter(); // Get the router instance

    const register = async () => {
      try {
        await axios.post("/register", {
          username: username.value,
          email: email.value,
          password: password.value,
        });
        successMessage.value = "Registration successful! You can now log in.";
        // Reset the form fields
        username.value = "";
        email.value = "";
        password.value = "";
        errors.value = {}; // Clear any previous errors
        // Redirect to the login page after successful registration
        router.push("/login");
      } catch (err) {
        errors.value = err.response.data; // Assuming the backend returns validation errors in this format
      }
    };

    return { username, email, password, register, errors, successMessage };
  },
};
</script>
