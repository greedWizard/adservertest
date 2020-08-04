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
    this.connect();
  },
  data() {
    return {
      messages: '',
      dialogue: '',
      newMessage: '',
      dialogueSocket: '',
    }
  },
  methods: {
    refreshMessages() {
      $.ajax({
        url: 'http://localhost:8000/api/chat/messages/',
        type: 'GET',
        async: false,
        data: {
          dialogue: this.$route.params.dialogue_id,
        },
        success: (response) => {
            this.messages = response.data.info;
            this.dialogue = this.messages[0].dialogue;

            console.log(this.dialogue);
        },
        error: (response) => {
          console.log(response);
        }
      });
    },
    connect() {
      this.dialogueSocket = new WebSocket('ws://0.0.0.0:8000/ws/dialogue/'+this.$route.params.dialogue_id);

      this.dialogueSocket.onopen = () => {
        this.refreshMessages();
        var refresh = this.refreshMessages;
        this.dialogueSocket.onmessage = function retrieve(event) {
          refresh();
        }
      };
    },
    sendMessage() {
      var recipient = -1;

      if(this.dialogue.seller.id===this.currentUser.id) {
        recipient = this.dialogue.buyer.id;
      }
      else {
        recipient = this.dialogue.seller.id;
      }

      var message_info = JSON.stringify(
        {
          'message': this.newMessage,
          'sender_id': this.currentUser.id,
          'recipient_id': recipient,
          'dialogue_id': this.$route.params.dialogue_id,
        }
      );

      this.dialogueSocket.send(message_info);

      this.newMessage = "";
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