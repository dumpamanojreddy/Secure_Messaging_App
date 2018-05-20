import { NgModule, ErrorHandler } from '@angular/core';
import { MyApp } from './app.component';
import { IonicApp, IonicModule, IonicErrorHandler } from 'ionic-angular';
import { Storage  } from '@ionic/storage';
import { TabsPage } from '../pages/tabs/tabs';
import { FriendsPage } from '../pages/friends/friends';
import { ConversationsPage} from '../pages/conversations/conversations';
import { AddFriendPage } from '../pages/add-friend/add-friend';
import { CreateConversationPage } from '../pages/create-conversation/create-conversation';
import { LoginPage } from '../pages/login/login';
import { RegisterPage } from '../pages/register/register';
import { AuthService } from '../providers/auth-service';
import { ConversationService } from '../providers/conversation-service'
import { UserPage } from '../pages/user/user';
import { AppPreferences } from '@ionic-native/app-preferences'
import { PrefService } from '../providers/pref-service'
import { ConversationPage } from '../pages/conversation/conversation'
import { CryptoService } from '../providers/crypto-service'
import { FriendService } from '../providers/friend-service'


@NgModule({
  declarations: [
    MyApp,
    TabsPage,
    FriendsPage,
    ConversationsPage,
    AddFriendPage,
    CreateConversationPage,
    LoginPage,
    RegisterPage, 
    UserPage,
    ConversationPage
  ],
  imports: [
    IonicModule.forRoot(MyApp),
  ],
  bootstrap: [IonicApp],
  entryComponents: [
    MyApp,
    TabsPage,
    FriendsPage,
    ConversationsPage,
    AddFriendPage,
    CreateConversationPage,
    LoginPage,
    RegisterPage,
    UserPage,
    ConversationPage
  ],
  providers: [Storage, AppPreferences, PrefService, AuthService, ConversationService, CryptoService, FriendService, {provide: ErrorHandler, useClass: IonicErrorHandler}]
})
export class AppModule {}
