<template>
  <div>
    <header-info> </header-info>
    <h3>Снять объявление?</h3>
    <ad> </ad>
    <hr>
    <p>После того, как вы нажмёте кнопку "подтвердить" восстановить объявление будет невозможно.</p>
    <button @click="deleteAd">Подтвердить</button>
  </div>
</template>

<script>
import $ from 'jquery'
import User from "../../mixins/User"
import Header from "../Header"
import Ad from "../board/Ad"

export default {
  name: 'Ads',
  data() {
      return {
          ad: '',
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
            },
            error: (response) => {
                alert(Ошибка);
            }
        });
      },
      deleteAd() {
          $.ajax({
              url: 'http://localhost:8000/api/board/ads/' + this.$route.params.ad_id,
              type: 'DELETE',
              success: (response) => {
                  alert('Объявление успешно удалено');
                  this.$router.push({name: 'index'});
              },
              error: (response) => {
                  alert('Не удалось произвести удаление');
              }
          })
      }
  },
  mixins: [
      User,
  ],
  components: {
      'header-info': Header,
      'ad': Ad,
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
