import { Component } from '@angular/core';
import { ConversationService } from '../../providers/conversation-service'
import { NavController, NavParams } from 'ionic-angular';

/*
  Generated class for the CreateConversation page.

  See http://ionicframework.com/docs/v2/components/#navigation for more info on
  Ionic pages and navigation.
*/
@Component({
  selector: 'page-create-conversation',
  templateUrl: 'create-conversation.html'
})
export class CreateConversationPage {
	private recipient: any;
	private message : any;
  constructor(public navCtrl: NavController, public navParams: NavParams, private  conversationService: ConversationService) {
      this.recipient = this.navParams.get('userName');
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad CreateConversationPage');
  
  }

  sendMessage()
  {
  	this.conversationService.sendMessage(this.recipient, this.message).then((res) => {
            //console.log("Sent message");
            this.navCtrl.pop();
        }, (err) => {
            console.log(err);
        });
  }
  

}
