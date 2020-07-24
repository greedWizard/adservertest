<template>
  <div class="index">
    <header-info> </header-info>
    <h2>Недавние объявление</h2>
    <ads :ads="ads"> </ads>
  </div>
</template>

<script>
import Ads from '../components/board/Ads'
import Header from '../components/Header'

import $ from 'jquery'

export default {
  name: 'Index',
  created() {
    this.getAds();
  },
  data () {
    return {
      ads: [],
    }
  },
  methods: {
    getAds() {
        $.ajax({
            async: false,
            url: 'http://localhost:8000/api/board/ads/',
            type: 'GET',
            success: (response) => {
                this.ads = response.data.info;
            },
            error: (response) => {
                console.error("Couldn't get ads");
                console.log(response);
            }
        })
    },
  },
  components: {
    'ads': Ads,
    'header-info': Header,
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
