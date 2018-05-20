import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';
import { AuthService } from '../../providers/auth-service';
import { LoginPage } from '../login/login';
import { App } from 'ionic-angular';

@Component({
	selector: 'page-user',
	templateUrl: 'user.html'
})

export class UserPage {

	constructor(private app: App,public navCtrl: NavController, public authService: AuthService, public navParams: NavParams) {}

	logout(){
		this.authService.logout();
        this.app.getRootNav().setRoot(LoginPage);
	}
}