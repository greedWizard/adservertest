<template>
  <div>
    <header-info> </header-info>
    <br>
    <div class="product-info">
      <a v-if="dialogue.ad"> 
        <img v-bind:src="'http://localhost:8000' + dialogue.ad.images[0].source" height="50" width="50">
        <a>{{ dialogue.ad.title }}</a>
        <a>{{ dialogue.ad.price }}р.</a>
      </a>
      <a v-else> 
        <p>Объявление удалено</p>
      </a>
      <hr>
      <a><a href="">{{ dialogue.seller.profile.first_name }}</a></a>
    </div>
    <div class="chat-area" style="border: 2px"> 
      <p v-for="message in this.messages" v-bind:key="message">
        <template v-if="!message.read">*</template>
        {{ message.sender.profile.first_name }}: {{ message.text }}
      </p>
      <a v-if="dialogue.ad"><input type="text" v-model="newMessage" @keypress.enter="sendMessage" placeholder="Введите сообщение"> <button @click="sendMessage">>>></button> </a>
    </div>
  </div>
</template>

<script>
import $ from 'jquery'
import Header from "../Header"
import User from '../../mixins/User'

export default {
  name: 'Dialogue',
  components: {
    'header-info': Header,
  },
  created() {
    this.loadUser();
    this.loadDialogue();
    setInterval(this.loadDialogue, 1000);
  },
  data() {
    return {
      messages: '',
      dialogue: '',
      newMessage: '',
    }
  },
  methods: {
    loadDialogue() {
      $.ajax({
        url: 'http://localhost:8000/api/chat/messages/',
        type: 'GET',
        data: {
          dialogue: this.$route.params.dialogue_id,
        },
        success: (response) => {
            this.messages = response.data.info;
            this.dialogue = this.messages[0].dialogue;
        },
        error: (response) => {
          
        }
      });
    },
    sendMessage() {
      var recipient = -1;

      if(this.dialogue.seller.id===this.currentUser.id) {
        recipient = this.dialogue.buyer.id;
      }
      else {
        recipient = this.dialogue.seller.id;
      }

      $.ajax({        
        url: 'http://localhost:8000/api/chat/messages/',
        type: 'POST',
        data: {
          dialogue: this.$route.params.dialogue_id,
          text: this.newMessage,
          recipient: recipient,
        },
        success: (resposne) => {
          this.newMessage = '';
        },
        error: (response) => {
          alert('Ошибка отправки сообщения');
        }
      });
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