<template>
  <div>
    <header-info> </header-info>

    <h3><a href="">{{ currentUser.profile.first_name }}</a> объявления</h3>

    <div class="ads user-ads" v-if="this.ads.length > 0"> 
      <ul> 
          <li v-for="ad in this.ads" v-bind:key="ad"> 
              <a @click="viewAd(ad.id)"><h3> {{ ad.title }} </h3></a>
              <img @click="viewAd(ad.id)" v-for="img in ad.images" v-bind:key="img" v-bind:src="'http://localhost:8000' + img.source" width="200px" height="200px"><br>
              <a v-if="currentUser.id===ad.author.id"> <br> <button>Снять объявление</button> <button>Редактировать</button> <br></a>
              <a v-else>  <br> <button>Откликнуться</button> <button>Пожаловаться</button>  <br></a>
              <span>  {{ ad.price }}p. </span>
              <span> {{ ad.adress.region.name }}, {{ ad.adress.region.city.name }} <a href="#">{{ ad.category.name }} </a></span>
              <p> {{ ad.desc.substring(0,100) }} </p>
          </li>
      </ul>
    </div>
    <div class="ads no-ads" v-else>
      <h3>Пользователь ещё не выложил ни одного объявления</h3>
    </div>

  </div>
</template>

<script>
import AdLoder from "../../mixins/AdLoader";
import User from '../../mixins/User'
import Header from '../Header'

import $ from 'jquery'

export default {
  data() {
      return {
          ads: [],
      }
  },
  name: 'AdsByUser',
  mixins: [
      User,
  ],
  created()
  {
    this.getAds();
    this.loadUser();
  },
  methods: {
    viewAd(ad_id) {
      this.$router.push({name: 'adDetails', params: {ad_id: ad_id}});
    },
    getAds(){
        $.ajax({
            url: 'http://localhost:8000/api/board/ads/by_user/' + this.$route.params.user_id,
            type: 'GET',
            success: (response) => {
                this.ads = response.data.info;
            },
            error: (response) => {
                alert('ошибка');
            }
        });
    },
  },
  components: {
      'header-info': Header,
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
