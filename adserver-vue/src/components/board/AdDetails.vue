<template>
  <div>
    <header-info> </header-info>
    <ad> </ad>
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
  },
  methods: {

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
