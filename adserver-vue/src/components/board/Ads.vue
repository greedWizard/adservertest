<template>
  <div>
    <ul> 
        <li v-for="ad in this.ads" v-bind:key="ad"> 
            <a @click="viewAd(ad.id)"><h3> {{ ad.title }} </h3></a>
            <img @click="viewAd(ad.id)" v-for="img in ad.images" v-bind:key="img" v-bind:src="'http://localhost:8000' + img.source" width="200px" height="200px"><br>
            <a v-if="currentUser">
              <a v-if="currentUser.id===ad.author.id"> <br> <button @click="goDelete(ad.id)">Снять объявление</button> <button @click="goEdit(ad.id)">Редактировать</button> <br></a>
              <a v-else>  <br> <button @click="startDialogue(ad.id)">Откликнуться</button> <button>Пожаловаться</button>  <br></a>
            </a>
            <span>  {{ ad.price }}p. </span> <br>
            <a href="#">{{ ad.author.profile.first_name }}</a>
            <span> {{ ad.adress.region.name }}, {{ ad.adress.region.city.name }} <a href="#">{{ ad.category.name }} </a></span>
            <p> {{ ad.desc.substring(0,100) }} </p>
        </li>
    </ul>
  </div>
</template>

<script>
import AdLoder from "../../mixins/AdLoader";
import User from '../../mixins/User'

import $ from 'jquery'

export default {
  name: 'Ads',
  mixins: [
      User,
  ],
  data() {
    return {
      
    }
  },
  props: [
    'ads',
  ],
  created()
  {
    this.loadUser();
  },
  methods: {
    viewAd(ad_id) {
      this.$router.push({name: 'adDetails', params: {ad_id: ad_id}});
    }, 
    goEdit(ad_id) {
      this.$router.push({name: 'editAd', params: {ad_id: ad_id}})
    },
    goDelete(ad_id) {
        this.$router.push({name: 'deleteAd', params: {ad_id: ad_id}})
    },
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
