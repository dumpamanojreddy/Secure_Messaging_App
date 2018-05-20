import { Component } from '@angular/core';
import { ViewChild} from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';
import { ConversationService } from '../../providers/conversation-service'

/*
  Generated class for the Conversation page.

  See http://ionicframework.com/docs/v2/components/#navigation for more info on
  Ionic pages and navigation.
*/
@Component({
  selector: 'page-conversation',
  templateUrl: 'conversation.html'
})

export class ConversationPage {
	userName : any;
	messages : any;
	replyMessage : any;
  constructor(public navCtrl: NavController, public navParams: NavParams, private conversationService: ConversationService) 
  {
  		this.userName = this.navParams.get('userName');
      //console.log("username: " + this.userName)
  		this.refresh();
  }

  ionViewDidLoad() {
    //console.log('ionViewDidLoad ConversationPage');
  }


  refresh(){
    this.conversationService.getMessages(this.userName).then((res) => {
          //console.log(res['response']);
              this.messages = res['response'];

          }, (err) => {
              console.log(err);
        });
  }

  reply(){
  	this.conversationService.sendMessage(this.userName, this.replyMessage).then((res) => {
            this.replyMessage = '';
            this.conversationService.getMessages(this.userName).then((res) => {
            //console.log(res['response']);
                this.messages = res['response'];
            }, (err) => {
                console.log(err);
          });
        }, (err) => {
            console.log(err);
        });
  }

}
