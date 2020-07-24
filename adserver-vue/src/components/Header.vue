<template>
  <div>
    <a href="/">ADSERVER</a>
    <a>
      <input type="text" @keypress.enter="fastSearch" v-model="searchTitle" placeholder="Быстрый поиск"> 
    </a>
    <a> 
      <input type="text" v-model="searchName" placeholder="Хочу найти...">
      <button @click="goSearch">Расширенный поиск</button>
    </a> <br>
    <a v-if="!this.currentUser">
      <button @click="goLogin">Вход</button>
      <button @click="goRegister">Регистрация</button>
    </a>
    <a v-if="this.currentUser"> 
      <button @click="goNewAd">Новое объявление</button>
      <button @click="goMyAds">Мои объявления</button>
      <button @click="goMyDialogues">Сообщения 
        <template v-if="newMessages.length > 0">
          (+{{ newMessages.length }})
        </template> 
      </button>
      <button @click="goProfile">Настройки</button>
      <button @click="logout">Выйти</button>
    </a>
  </div>
</template>

<script>
import $ from 'jquery'

import User from '../mixins/User'
import AdUtils from '../mixins/AdsUtils'

export default {
  name: 'Header',
  data () {
    return {
      categories: [],
      searchName: '',
      searchCategory: '',
      searchTitle: '',
    }
  },
  created(){
    this.loadUser();
    this.loadCategories();
    this.loadNewMessages();
    setInterval(this.loadNewMessages, 5000);
  },
  methods: {
    goLogin() {
      this.$router.push({name: 'login'});
    },
    logout(){
      localStorage.removeItem('auth_token');
      this.currentUser = undefined;
      this.$router.push({name: 'index'});
    },
    goRegister(){
      this.$router.push({name: 'registration'});
    },
    goProfile(){
      this.$router.push({name: 'profile'});
    },
    goNewAd(){
      this.$router.push({name: 'createAd'});
    },
    goMyAds() {
      this.$router.push({name: 'adsByUser', params: {user_id: this.currentUser.id}});
    },
    goMyDialogues() {
      this.$router.push({name: 'myDialogues'});
    },
    goSearch() {
      this.$router.push({name: 'search'});
    },
    fastSearch() {
      $.ajax({
        url: 'http://localhost:8000/api/board/ads/',
        type: 'GET',
        data: {
          title: this.searchTitle,
        },
        success: (response) => {
          this.$router.push({name: 'search', query: {title: this.searchTitle}});
        }
      });
    }
  },
  mixins: [
    User,
    AdUtils,
  ]
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
