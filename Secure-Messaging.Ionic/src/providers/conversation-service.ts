import { Injectable } from '@angular/core';
import { Http, Response, Headers, RequestOptions  } from '@angular/http';
import { AuthService } from './auth-service';
import { PrefService } from './pref-service';
import { CryptoService } from './crypto-service';
import { Storage } from '@ionic/storage';
import 'rxjs/add/operator/map';
 
@Injectable()
export class ConversationService {
 
  constructor(public http: Http, private prefs : PrefService, private auth : AuthService, 
	private storage: Storage, private cryptoService : CryptoService) {
 		
	}
	sendMessage(recipient, message){ 
    	return new Promise((resolve, reject) => {
			if(message == "" || message == null){
				reject("Invalid message");
			}
			let token = this.auth.token;
    		let headers = new Headers();
			headers.append('username', recipient);
			this.getUsersPublicKey(recipient).then((res) => {
				if(res != null && res != ''){
					let usersPublicKey = res;
					headers = new Headers();
					headers.append('recipient', recipient);
					headers.append('token', token);
					let encryptionKey = this.cryptoService.generateSecretKey(this.cryptoService.privateKey, usersPublicKey);
					let encrypted = this.cryptoService.AESEncrypt(message, encryptionKey);	 
					headers.append('iv', JSON.stringify(encrypted.IV));
					this.http.post(this.prefs.baseURL + '/sendMessage', encrypted.data, { headers: headers})
		          			.subscribe(res => {		 
					            let data = res.json();
					            resolve(data);
					          }, (err) => {
					            reject(err);
					         }); 
				}
				else{
					reject("Invalid public key");
				}
			});	
    	});
 
  	}

	getConversations(){ 
    	return new Promise((resolve, reject) => {
        	let token = this.auth.token;
    		let headers = new Headers();
			headers.append('token', token);
 			this.http.get(this.prefs.baseURL + '/getConversations', { headers : headers})
				.subscribe(res => {
					let data = res.json();
					resolve(data);
				}, (err) => {
					reject(err);
				});
 
    	});
   	}
	
	getMessages(userName){
		return new Promise((resolve, reject) => {
        	let token = this.auth.token;
    		let headers = new Headers();
			headers.append('token', token);
			headers.append('conversation', userName);
			this.getUsersPublicKey(userName).then((res) => {
				if(res != null){
					let usersPublicKey = res;
					this.http.get(this.prefs.baseURL + '/getMessages', { headers : headers})
						.subscribe(res => {
							let data = res.json();
							let decryptKey = this.cryptoService.generateSecretKey(this.cryptoService.privateKey, usersPublicKey);
							for(let message of data['response']){
								let encryptedMessage = JSON.parse(message['message']);
								let iv = JSON.parse(message['iv']);
								message['message'] = this.cryptoService.AESDecrypt(encryptedMessage, decryptKey, iv);					
								let utcSeconds = message['timestamp'];
								let d = new Date(0); // The 0 there is the key, which sets the date to the epoch
								d.setUTCSeconds(utcSeconds);
								let hours = d.getHours();
							  	let minutes : any  = d.getMinutes();
							  	let ampm = hours >= 12 ? 'pm' : 'am';
							  	hours = hours % 12;
							  	hours = hours ? hours : 12; // the hour '0' should be '12'
							  	minutes = minutes < 10 ? '0' + minutes : minutes;
							 	let strTime = hours + ':' + minutes + ' ' + ampm;
							  	message['timestamp'] = d.getMonth()+1 + "/" + d.getDate() + "/" + d.getFullYear() + "  " + strTime;
							}						

							resolve(data);				
						}, (err) => {
							reject(err);
					});						
				}
				else{
				reject("Invalid public key")
				}
			});
    	});

	}

	private getUsersPublicKey(username){
		return new Promise((resolve, reject) => {
			let token = this.auth.token;
    		let headers = new Headers();
			headers.append('token', token);
			headers.append('username', username);
			this.http.get(this.prefs.baseURL + '/getUsersPublicKey', {headers : headers})
				.subscribe(res => {
					resolve(res.json()['response'])
				}, (err) => {
					reject(err);
			});
		});

	}
}