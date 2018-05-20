import { Component } from '@angular/core';
import { NavController, LoadingController } from 'ionic-angular';
import { AuthService } from '../../providers/auth-service';
import { TabsPage } from '../tabs/tabs';
import { RegisterPage } from '../register/register';
import {CryptoService } from '../../providers/crypto-service'
 
@Component({
  selector: 'login-page',
  templateUrl: 'login.html'
})
export class LoginPage {
 
    username: string;
    password: string;
    loading: any;

 
    constructor(public navCtrl: NavController, public authService: AuthService, public loadingCtrl: LoadingController,
        private cryptoService : CryptoService) {
 
    }
 
    ionViewDidLoad() {
 
        this.showAuthenticatingLoader();
 
        //Check if already authenticated
        this.authService.checkAuthentication().then((res) => {
            //console.log("Already authorized");
            this.loading.dismiss();
            this.navCtrl.setRoot(TabsPage);
        }, (err) => {
            console.log("Not already authorized");
            this.loading.dismiss();
        });
 
    }
 
    login(){
 
        this.showAuthenticatingLoader();
 
        let credentials = {
            username: this.username,
            password: this.password
        };

        this.cryptoService.serverHandshake().then((handshakeResult) => {
            this.authService.login(credentials, handshakeResult).then((result) => {
            this.loading.dismiss();
            //console.log(result);
            credentials = null;
            this.navCtrl.setRoot(TabsPage);
        }, (err) => {
            this.loading.dismiss();
            console.log(err);
        });
        }, (err) => {
            this.loading.dismiss();
            console.log(err);
        }); 
    }
 
    register(){
        this.navCtrl.push(RegisterPage);
    }
 
    showAuthenticatingLoader(){
 
        this.loading = this.loadingCtrl.create({
            content: 'Authenticating...'
        });
 
        this.loading.present();
 
    }
    showLoginError(){
 
    }
 
}