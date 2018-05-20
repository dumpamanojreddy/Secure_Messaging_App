import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';
import { FriendService } from '../../providers/friend-service'

/*
  Generated class for the AddFriend page.

  See http://ionicframework.com/docs/v2/components/#navigation for more info on
  Ionic pages and navigation.
*/
@Component({
  selector: 'page-add-friend',
  templateUrl: 'add-friend.html'
})
export class AddFriendPage {

  searchQuery: string = '';
  users: any;
  filteredUsers : any;
  constructor(public navCtrl: NavController, public navParams: NavParams, private friendService : FriendService) {
    friendService.getUsers().then((res) => {
        console.log(res);
        this.users = res;
        this.filteredUsers = this.users;
    });
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad AddFriendPage');
  }
  addFriend(userName){
    console.log("add friend " + userName);
    this.friendService.addFriend(userName);
    this.navCtrl.pop();
  }
  searchUser(ev: any) {

    // set val to the value of the searchbar
    let val = ev.target.value;
    if(val.trim() == ''){
      this.filteredUsers = this.users;
    }
    // if the value is an empty string don't filter the users
    if (val && val.trim() != '') {
    	if (this.users != null)
    	{
	      this.filteredUsers = this.users.filter((item) => {
	      	  return (item.toLowerCase().indexOf(val.toLowerCase()) > -1);
	      })
  		}
    }
  }
}
