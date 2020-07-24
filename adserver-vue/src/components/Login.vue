<template>
  <div class="index">
    <h2>Введите имя пользователя и пароль</h2>
    <input v-model="username" placeholder="имя пользователя">
    <input v-model="password" type="password" placeholder="пароль"> 
    <button @click="tryLogin">Войти</button>
  </div>
</template>

<script>
import $ from 'jquery'

export default {
  name: 'HelloWorld',
  data() {
    return {
      username: '',
      password: '',
    }
  },
  methods: {
      tryLogin()
      {
          $.ajax({
              url: 'http://localhost:8000/api/auth/token/login',
              type: 'POST',
              data: {
                  username: this.username,
                  password: this.password,
              },
              success: (response) =>
              {
                  localStorage.setItem('auth_token', response.data.attributes.auth_token);
                  alert('Успешный вход');
                  this.$router.push({name: 'index'});
              },
              error: (response) => {
                  alert('Не удалось войти');
              }
          })
      }
  }
}
</script>

<style scoped>
</style>
