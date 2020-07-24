<template>
  <div>
    <header-info> </header-info>
    <h2>Мои сообщения</h2>
    <ul> 
      <div class="message">
        <li v-for="message in this.lastMessages" v-bind:key="message">
          <a v-if="message.dialogue.ad"> 
            <p><img v-bind:src="'http://localhost:8000' + message.dialogue.ad.images[0].source" height="100" width="100"></p>
            <span>{{ message.dialogue.ad.title }}</span>
          </a>
          <a v-else> 
            <span>Объявление удалено</span>
          </a>
          <p>{{ message.dialogue.buyer.profile.first_name }}</p>
          <p>
            <template v-if="!message.read">*</template>
            {{ message.sender.profile.first_name }}: {{ message.text }}
          </p>
          
          <button @click="goDialogue(message.dialogue.id)">Перейти в диалог</button>
        </li>
      </div>
    </ul>
  </div>
</template>

<script>
import $ from 'jquery'
import Header from "../Header"
import User from '../../mixins/User'

export default {
  name: 'MyDialogues',
  components: {
    'header-info': Header,
  },
  created() {
    this.loadUser();
    this.loadLastMessages();
  },
  data() {
    return {
      lastMessages: [],
    }
  },
  methods: {
    goDialogue(dialogue_id) {
      this.$router.push({name: 'dialogue', params: {dialogue_id: dialogue_id}})
    }
  },
  mixins: [
    User,
  ]
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>