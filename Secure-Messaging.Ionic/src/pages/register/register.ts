import { Component } from '@angular/core';
import { NavController, LoadingController } from 'ionic-angular';
import { AuthService } from '../../providers/auth-service';
import { TabsPage } from '../tabs/tabs';
import { CryptoService } from '../../providers/crypto-service';
 
@Component({
  selector: 'register-page',
  templateUrl: 'register.html'
})
export class RegisterPage {
	firstName : string;
	lastName : string;
  username: string;
  password: string;
  confirmPassword : string;
  loading : any;
 
  constructor(public navCtrl: NavController, public authService: AuthService, public loadingCtrl: LoadingController, private cryptoService : CryptoService) {
 
  }
 
  register(){
 
    this.showLoader();
 
    let credentials = {
        username: this.username,
        password: this.password
    };
 
    this.cryptoService.serverHandshake().then((handshakeResult) => {
            this.authService.login(credentials, handshakeResult).then((result) => {
            this.loading.dismiss();
            //console.log(result);
            credentials = null;
            this.navCtrl.pop();
            }, (err) => {
                this.loading.dismiss();
                console.log(err);
            });
        }, (err) => {
            this.loading.dismiss();
            console.log(err);
        }); 
 
  }
 
  showLoader(){
 
    this.loading = this.loadingCtrl.create({
      content: 'Registerting...'
    });
 
    this.loading.present();
 
  }
 
}