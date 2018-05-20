import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';
import { AddFriendPage } from '../add-friend/add-friend';
import { FriendService } from '../../providers/friend-service';
import { CreateConversationPage } from '../create-conversation/create-conversation'

/*
  Generated class for the Friends page.

  See http://ionicframework.com/docs/v2/components/#navigation for more info on
  Ionic pages and navigation.
*/
@Component({
  selector: 'page-friends',
  templateUrl: 'friends.html'
})


export class FriendsPage {
  friends :any;
  constructor(public navCtrl: NavController, public navParams: NavParams, public friendService : FriendService) {
      
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad FriendsPage');
    
  }

  ionViewWillEnter(){
    this.friendService.getFriends().then((res) => {
          //console.log(res['response']);
              this.friends = res;
              console.log(this.friends);
          }, (err) => {
              console.log(err);
        });
  }


	addFriend() {
  //push another page onto the history stack
  //causing the nav controller to animate the new page in
  this.navCtrl.push(AddFriendPage);
  }

  newConversation(userName){
    //push another page onto the history stack
    //causing the nav controller to animate the new page in
    this.navCtrl.push(CreateConversationPage, {"userName" : userName});
  }

}
