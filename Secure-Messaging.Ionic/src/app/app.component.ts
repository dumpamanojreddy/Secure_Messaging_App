import { Component } from '@angular/core';
import { Platform } from 'ionic-angular';
import { StatusBar, Splashscreen } from 'ionic-native';
import { LoginPage } from '../pages/login/login';
import { PrefService } from '../providers/pref-service';

@Component({
  templateUrl: 'app.html'
})
export class MyApp {
  private rootPage;

  constructor(platform: Platform, preferences: PrefService) {
    console.log("My app constructor");
    this.rootPage = LoginPage;
    platform.ready().then(() => {
      // Okay, so the platform is ready and our plugins are available.
      // Here you can do any higher level native things you might need.
      StatusBar.styleDefault();
      Splashscreen.hide();
      preferences.getPreferences();
    });
  }
}
