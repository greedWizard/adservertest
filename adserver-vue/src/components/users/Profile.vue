<template>

  <div>
      <header-info> </header-info>
    <h2>Настройки профиля</h2>
    <div> 
        <a> <button id="main-button" disabled @click="showMainInfo">Основные данные</button> </a>
        <a> <button id="profile-button" @click="showProfileInfo">Данные пользователя</button> </a>
    </div>
    <div id="main-info"> 
      <h3>Основные данные</h3>
      <a> <p id="login_text"> Имя пользователя: </p> <input v-model="username" placeholder="Имя пользователя"> </a> 
      <a><p id="email_text"> Адресс электронной почты: </p> <input v-model="email" type="email" placeholder="email"> </a> 
      <a><p id="password_text"> * Пароль: </p> <input v-model="password" type="password" placeholder="Пароль"></a> 
      <a><p id="password2_text"> * Пароль повторно: </p> <input v-model="password2" type="password" placeholder="Повторите пароль"></a>
      <a><p id="password_text"> Новый пароль: </p> <input v-model="new_password" type="password" placeholder="Пароль"></a> 
      <a><p id="password2_text"> Новый пароль повторно: </p> <input v-model="new_password2" type="password" placeholder="Повторите пароль"></a> 
      <br> <br>
      <a><button @click="updateUser">Сохранить</button></a>
    </div>
    <div id="profile-info" hidden>
        <h3>Персональные данные</h3>
        <a><h3>Фотография</h3></a>
        <img v-bind:src="this.profile_pic" id="profile_picture" width="400px" height="400px" style="border-radius: 50%">
        <input type="file" @change="uploadProfilePic" accept="image/"> 
        <a> </a>
        <a><p id="first_name_text"> * Имя: </p> <input v-model="first_name" type="text" placeholder="Имя"></a> 
        <a><p id="last_name_text"> * Фамилия: </p> <input v-model="last_name" type="text" placeholder="Фамилия"></a> 
        <a><p id="phone_number_text"> * Номер телефона: (+)</p> <input v-model="phone_number" type="text" placeholder="Номер телефона"></a> <br> <br>
        <button @click="updateProfile">Сохранить</button>
    </div>
  </div>
</template>

<script>
import $ from 'jquery'
import Header from '@/components/Header'
import User from '../../mixins/User'

export default {
  name: 'Profile',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      password2: '',
      new_password: '',
      new_password2: '',
      firts_name: '',
      last_name: '',
      phone_number: '',
      profile_pic: null,
      new_profile_pic: null,
    }
  },
  methods: {
      fillGaps()
      {
          this.username = this.currentUser.username;
          this.email = this.currentUser.email;
          this.first_name = this.currentUser.profile.first_name;
          this.last_name = this.currentUser.profile.last_name;
          this.phone_number = this.currentUser.profile.phone_number;
          this.profile_pic = 'http://localhost:8000' + this.currentUser.profile.profile_pic;
      },
      showProfileInfo()
      {
          let main_info = document.getElementById('main-info');
          main_info.hidden = true;

          let profile_info = document.getElementById('profile-info');
          profile_info.hidden = false;

          let main_button = document.getElementById('main-button');
          main_button.disabled = false;

          let profile_button = document.getElementById('profile-button');
          profile_button.disabled = true;
      },
      showMainInfo()
      {
          let main_info = document.getElementById('main-info');
          main_info.hidden = false;

          let profile_info = document.getElementById('profile-info');
          profile_info.hidden = true;

          let main_button = document.getElementById('main-button');
          main_button.disabled = true;

          let profile_button = document.getElementById('profile-button');
          profile_button.disabled = false;
      },
      updateUser()
      {
          var new_data = {
              'username': this.username,
              'email': this.email,
              'password': this.password,
              'password2': this.password2,
          };

          if(this.new_password){
              new_data['new_password'] = this.new_password;
              new_data['new_password2'] = this.new_password2;
          }

          $.ajax({
              url: 'http://localhost:8000/api/users/update/',
              type: 'POST',
              data: new_data,
              async: true,
              success: (response) => {
                  console.log(response);
                  alert('Основные данные успешно обновлены');
              },
              error: (response) => {
                  alert('Не удалось обновить данные профиля');
              },
          });
      },
      updateProfile()
      {
          var formData = new FormData();
          
          if(this.new_profile_pic)
          {
              formData.append('profile_pic', this.new_profile_pic, this.new_profile_pic.name);
          }

          formData.append('first_name', this.first_name);
          formData.append('last_name', this.last_name);
          formData.append('phone_number', this.phone_number);

          $.ajax({
              url: 'http://localhost:8000/api/users/profile/update/',
              type: 'POST',
              processData: false,
              contentType: false,
              data: formData,
              success: (response) => {
                  alert('Данные успешно обновлены');
              },
              error: (response) => {
                  console.log(response);
                  alert('Не удалось обновить данные профиля');
              }
          });
      },
      uploadProfilePic(e)
      {
          this.new_profile_pic = e.target.files[0];
      }
  },
  components: {
      'header-info': Header,
  },
  created()
  {
      this.loadUser();
      if(!this.currentUser){
          this.$router.push({name: 'login'})
      }
      this.fillGaps();
  },
  mixins: [
      User,
  ]
}
</script>

<style>

</style>
