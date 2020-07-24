import $ from 'jquery'

export default {
    data()
    {
        return {
            currentUser: undefined,
            newMessages: [],
        }
    },
    methods: {
        loadUser() {
            $.ajax({
                async: false,
                url: 'http://localhost:8000/api/users/profile/',
                type: 'GET',
                success: (response) => {
                    this.currentUser = response.data.info;

                },
                error: (response) => {
                    console.error('Not authenticated');
                    console.log(response);
                    this.currentUser = undefined;
                }
            })
        },
        startDialogue(ad_id) {
            $.ajax({
                url: 'http://localhost:8000/api/chat/dialogues/',
                type: 'GET',
                success: (response) => {
                var new_messages = response.data.info;
                var dialogueExists = false;
                var dialogue_id = -1;
                for(var i = 0; i < new_messages.length; i++) {
                    try {
                        if(new_messages[i].dialogue.ad.id===ad_id && new_messages[i].dialogue.buyer.id===this.currentUser.id) {
                        dialogueExists = true;
                        dialogue_id = new_messages[i].dialogue.id;
                        break;
                    }
                    } catch(TypeError) {
        
                    }
                }
        
                if(dialogueExists) {
                    this.$router.push({name: 'dialogue', params: {dialogue_id: dialogue_id}});
                }
                else {
                    $.ajax({
                    url: 'http://localhost:8000/api/chat/dialogues/',
                    type: 'POST',
                    data: {
                        ad: ad_id,
                    },
                    success: (response) => {
                        this.$router.push({name: 'dialogue', params: {dialogue_id: response.data.created_dialogue}});
                    },
                    error: (response) => {
                        console.log(response);
                    }
                    });
                }
                }
            });
        },
        loadLastMessages() {
            if(this.currentUser.id) {
                $.ajax({
                url: 'http://localhost:8000/api/chat/dialogues/',
                type: 'GET',
                success: (response) => {
                    this.lastMessages = response.data.info;
                    console.log(this.dialogues);
                },
                error: (response) => {
                    alert('Не удалось загрузить сообщения.')
                }
                });
            }
        },
        loadNewMessages() {
            if(this.currentUser.id) {
                var previousMessages = this.newMessages;

                var newMsgs = [];
                $.ajax({
                    url: 'http://localhost:8000/api/chat/messages/new/',
                    type: 'GET',
                    success: (response) => {
                        var messages = response.data.info;

                        for(var i=0; i<messages.length; i++) {
                            if(messages[i].sender.id != this.currentUser.id) {
                                newMsgs.push(messages[i]);
                            }
                        }

                        if(newMsgs.length > previousMessages.length) {
                            this.newMessages = newMsgs;
                        }
                    },
                    error: (response) => {
                        
                    }
                });
            }
        }
    }
}