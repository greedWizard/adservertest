<template>
  <div id="app">
    <h2>Новый пользователь</h2>
    <div id="main-info"> 
      <h3>Основные данные</h3>
      <a> <p id="login_text"> * Имя пользователя: </p> <input v-model="login" placeholder="Имя пользователя"> </a> <br> <br>
      <a><p id="email_text"> * Адресс электронной почты: </p> <input v-model="email" type="email" placeholder="email"> </a> <br> <br>
      <a><p id="password_text"> * Пароль: </p> <input v-model="password" type="password" placeholder="Пароль"></a> <br> <br>
      <a><p id="password2_text"> * Пароль повторно: </p> <input v-model="password2" type="password" placeholder="Повторите пароль"></a> <br> <br>
      <button @click="hideMainInfo">Продолжить</button>
    </div>
    <div id="profile-info" style="display: none;">
        <h3>Пожалуйста, заполните персональные данные</h3>
        <a><p id="first_name_text"> * Имя: </p> <input v-model="first_name" type="text" placeholder="Имя"></a> <br> <br>
        <a><p id="last_name_text"> * Фамилия: </p> <input v-model="last_name" type="text" placeholder="Фамилия"></a> <br> <br>
        <a><p id="phone_number_text"> * Номер телефона: (+)</p> <input v-model="phone_number" type="text" placeholder="Номер телефона"></a> <br> <br>
        <button @click="completeRegister">Регистрация</button>
    </div>
  </div>
</template>

<script>
import $ from 'jquery'

export default {
  name: 'Profile',
  data() {
    return {
      login: '',
      email: '',
      password: '',
      password2: '',
    }
  },
  methods: {
    hideMainInfo()
    {
      var unfilled = false;

      if(!this.login)
      {
        let login_text = document.getElementById('login_text');
        login_text.style.color = 'red';
        unfilled = true;
      }
      if(!this.email)
      {
        let email_text = document.getElementById('email_text');
        email_text.style.color = 'red';
        unfilled = true;
      }
      if(!this.password)
      {
        let password_text = document.getElementById('password_text');
        password_text.style.color = 'red';
        unfilled = true;
      }
      if(!this.password2)
      {
        let password2_text = document.getElementById('password2_text');
        password2_text.style.color = 'red';
        unfilled = true;
      }

      if(unfilled){
        return;
      }

      let main_info = document.getElementById('main-info');
      main_info.style.display = 'none';

      let profile_info = document.getElementById('profile-info');
      profile_info.style.display = 'block';
    },
    completeRegister()
    {
      $.ajax({
        url: 'http://localhost:8000/api/users/register/',
        type: 'POST',
        data: {
          username: this.login,
          password: this.password,
          password2: this.password2,
          first_name: this.first_name,
          last_name: this.last_name,
          phone_number: this.phone_number,
          email: this.email,
        },
        success: (response) => {
          alert('Регистрация успешна');
          console.log(response);
          this.$router.push({name: 'index'});
        },
        error: (response) => {
          console.error('Не удалось зарегестрировать пользователя');
          console.error(response);
        }
      })
    }
  }
}
</script>

<style>

</style>
