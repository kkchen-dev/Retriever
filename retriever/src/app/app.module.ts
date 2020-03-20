import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MaterialModule } from './material.module';
import { TopBarComponent } from './top-bar/top-bar.component';
import { HttpClientModule } from '@angular/common/http';
import { FeedComponent } from './feed/feed.component';
import { FeedsComponent } from './feeds/feeds.component';


@NgModule({
  declarations: [
    AppComponent,
    TopBarComponent,
    FeedComponent,
    FeedsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
