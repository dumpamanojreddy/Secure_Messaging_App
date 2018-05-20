import { Component } from '@angular/core';
import { ConversationsPage } from '../conversations/conversations';
import { FriendsPage } from '../friends/friends';
import { UserPage } from '../user/user';


@Component({
  templateUrl: 'tabs.html'
})

export class TabsPage {
  // this tells the tabs component which Pages
  // should be each tab's root Page
  tab1Root = ConversationsPage;
  tab2Root = FriendsPage;
  tab3Root = UserPage;

  constructor() {

  }
}