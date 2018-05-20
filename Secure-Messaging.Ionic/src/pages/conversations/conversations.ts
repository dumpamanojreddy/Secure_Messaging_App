import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';
import { CreateConversationPage } from '../create-conversation/create-conversation';
import { ConversationService } from '../../providers/conversation-service';
import { ConversationPage } from '../conversation/conversation';

/*
  Generated class for the Conversations page.

  See http://ionicframework.com/docs/v2/components/#navigation for more info on
  Ionic pages and navigation.
*/
@Component({
  selector: 'page-conversations',
  templateUrl: 'conversations.html'
})
export class ConversationsPage {

  private conversations : any;

  constructor(public navCtrl: NavController, public navParams: NavParams, private conversationService: ConversationService) 
  {
       
  }

  ionViewWillEnter()
  {
    this.conversationService.getConversations().then((res) => {
            //console.log(res['response']);
            this.conversations = res['response'];
        }, (err) => {
            console.log(err);
        });
  }


  ionViewDidLoad() {
    //console.log('ionViewDidLoad ConversationsPage');
  }

  createConversation() {
    //push another page onto the history stack
    //causing the nav controller to animate the new page in
    this.navCtrl.push(CreateConversationPage);
  }

  openConversation(userName){
     
      this.navCtrl.push(ConversationPage, {
            "userName": userName,
          });
  }
  

}
