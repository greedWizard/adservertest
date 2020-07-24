<template>

  <div>
      <header-info> </header-info>
    <h2>{{ this.selectedUser.profile.first_name }}</h2>
    <div id="profile-info" hidden>
         
    </div>
  </div>
</template>

<script>
import $ from 'jquery'
import Header from '@/components/Header'
import User from '../../mixins/User'

export default {
  name: 'AnotherProfile',
  data() {
    return {

    }
  },
  methods: {
      loadSelectedUser() {

      }
  },
  components: {
      'header-info': Header,
  },
  created()
  {
      this.loadUser();
  },
  mixins: [
      User,
  ]
}
</script>

<style>

</style>
