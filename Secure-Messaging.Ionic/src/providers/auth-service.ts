import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions  } from '@angular/http';
import { PrefService } from './pref-service'
import { Storage } from '@ionic/storage';
import { CryptoService } from './crypto-service';
import * as CryptoJS from '../../node_modules/crypto-js'
import 'rxjs/add/operator/map';
 
@Injectable()
export class AuthService {
 
  public token: any;
 
  constructor(public http: Http, private prefs : PrefService, private cryptoService : CryptoService, public storage: Storage) {
 
	}
 
	checkAuthentication(){
 
    return new Promise((resolve, reject) => {
 
        //Load token if exists
        this.storage.get('token').then((value) => {
 
            this.token = value;

			if(this.token != ''){
				reject();
			}
			else{
				reject();
			}
 
        });         
 
    });
 
  }
 
	createAccount(details){
 
    return new Promise((resolve, reject) => {
 
        let headers = new Headers();
        headers.append('Content-Type', 'application/json');
 
        this.http.post(this.prefs.baseURL + '/register', JSON.stringify(details), {headers: headers})
          .subscribe(res => {
 
            let data = res.json();
            this.token = data.token;
            this.storage.set('token', data.token);
            resolve(data);
 
          }, (err) => {
            reject(err);
          });
 
    });
 
  }
 
 	login(credentials, handshakeData){
 
    return new Promise((resolve, reject) => {
		let hashPassword = CryptoJS.SHA1(credentials.password).toString();
		let encryptedData = this.cryptoService.AESEncrypt(hashPassword, this.cryptoService.symetricServerKey);
 		let headers = new Headers();
		headers.append('username', credentials.username);
		headers.append('password', JSON.stringify(encryptedData.data));
		headers.append('IV', JSON.stringify(encryptedData.IV));
		headers.append('tempHandshakeId',handshakeData['response']);
        this.http.post(this.prefs.baseURL + '/login', null,{ headers: headers})
          .subscribe(res => {
 
            let data = res.json();
           	this.cryptoService.privateKey = this.cryptoService.AESDecrypt(data.privateKey, this.cryptoService.symetricServerKey, data.iv);
			this.storage.set('token', data.token).then(() => {
				this.token = data.token;
				resolve(data);
			});
          }, (err) => {
			reject(err);
          }); 
    });
 
  }
 
  logout(){
    this.storage.set('token', '');
	this.token = null;
  }
 
}