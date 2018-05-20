import { Injectable } from '@angular/core';
import { Http, Response, Headers  } from '@angular/http';
import { AuthService } from './auth-service';
import { PrefService } from './pref-service';
import { Storage } from '@ionic/storage';
import { CryptoService } from './crypto-service'
import 'rxjs/add/operator/map';
 
@Injectable()
export class FriendService {
 
	friends: any;
	users: any;
  constructor(public http: Http, private auth : AuthService, private prefs : PrefService, private crypto : CryptoService, private storgae : Storage) {
 		
	}

	getFriends(){
		return new Promise((resolve, reject) => {			
	        let token = this.auth.token;
    		let headers = new Headers();
			headers.append('token', token);		
	 
	        this.http.get(this.prefs.baseURL + '/getFriends', { headers: headers})
	          .subscribe(res => {
	 
	            let friends = res.json()['response'];
	            resolve(friends);
	          }, (err) => {
	            reject(err);
	          });  
		});
	}

	getUsers(){
		return new Promise((resolve, reject) => {			
	        let token = this.auth.token;
    		let headers = new Headers();
			headers.append('token', token);		
	 
	        this.http.get(this.prefs.baseURL + '/getUsers', { headers: headers})
	          .subscribe(res => {
	 
	            let users = res.json()['response'];
	            resolve(users);
	          }, (err) => {
	            reject(err);
	          });  
		});
	}

	addFriend(userName){
		return new Promise((resolve, reject) => {			
	        let token = this.auth.token;
    		let headers = new Headers();
			headers.append('token', token);
			headers.append('friend', userName);		
	 
	        this.http.get(this.prefs.baseURL + '/addFriend', { headers: headers})
	          .subscribe(res => {
				let data = res.json();
				this.storgae.set(userName + "Key", this.crypto.generateSecretKey(this.crypto.privateKey, data['response']))
	            resolve();
	          }, (err) => {
	            reject(err);
	          });  
		});
	}
	
}