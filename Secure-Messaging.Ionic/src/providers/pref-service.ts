import { Injectable } from '@angular/core';
import { Platform } from 'ionic-angular';
import { AppPreferences } from '@ionic-native/app-preferences'

@Injectable()
export class PrefService {
 	public host : string;
	public port : any;
	public sslEnabled : any;
	public baseURL : string;
	constructor(private pref : AppPreferences, private plat : Platform) {
		this.host = 'localhost';
		this.port = 8081;
		this.sslEnabled = false;
			
	}

	getPreferences()
	{
		if(this.plat.is('mobile')){
			 	this.pref.fetch('host').then((res) => { 
					this.host = res;
					});
				this.pref.fetch('port').then((res) =>{
				});
				this.pref.fetch('sslEnabled').then((res) => {
					this.sslEnabled = res;
				});
		}

			if(this.sslEnabled == true){
				this.baseURL = 'https://';
			}
			else{
				this.baseURL = 'http://';
			}

			if(this.host != '' && this.host != null){
				this.baseURL = this.baseURL.concat(this.host);
			}
			else{
				this.baseURL = this.baseURL.concat('localhost');
			}	
			if(this.port != '' && this.port != null){
				this.baseURL = this.baseURL.concat(':' + this.port );
			}
	}
}