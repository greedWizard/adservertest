<template>
  <div>
    <!-- <header-info> </header-info> -->
    <h3> {{ ad.title }}  </h3>
    <img v-for="img in ad.images" v-bind:key="img"  v-bind:src="'http://localhost:8000' + img.source" width="200px" height="200px"><br>
    <a v-if="currentUser">
        <a v-if="currentUser.id===ad.author.id"> <br> <button @click="goDelete(ad.id)">Снять объявление</button> <button @click="goEdit(ad.id)">Редактировать</button> <br></a>
        <a v-else>  <br> <button>Откликнуться</button> <button>Пожаловаться</button>  <br></a>
    </a>
    <span>  {{ ad.price }}p. </span>
    <span> {{ ad.adress.region.name }}, {{ ad.adress.region.city.name }} <a href="#">{{ ad.category.name }} </a></span>
    <p> {{ ad.desc.substring(0,100) }} </p>
    <hr>
    <p>Информация о товаре: </p>
    <p>Категория: <a href="#">{{ ad.category.name }}</a></p>
    <p v-for="field in necessaryFields" v-bind:key="field">{{ field.name }}: {{ ad.data[field.name] }}</p>
  </div>
</template>

<script>
import $ from 'jquery'
import User from "../../mixins/User"
import Header from "../Header"

export default {
  name: 'Ads',
  data() {
      return {
          ad: '',
          necessaryFields: [],
      }
  },
  created() {
      this.loadUser();
      this.loadAd();
  },
  methods: {
      loadAd() {
            $.ajax({
                url: 'http://localhost:8000/api/board/ads/' + this.$route.params.ad_id,
                type: 'GET', 
                success: (response) => {
                    this.ad = response.data.info;
                    this.necessaryFields = this.ad.category.necessary_fields;
                },
                error: (response) => {
                    alert(Ошибка);
                }
            });
        },
        goEdit(ad_id) {
            this.$router.push({name: 'editAd', params: {ad_id: ad_id}})
        },
        goDelete(ad_id) {
            this.$router.push({name: 'deleteAd', params: {ad_id: ad_id}})
        }
  },
  mixins: [
      User,
  ],
  components: {
      'header-info': Header,
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
