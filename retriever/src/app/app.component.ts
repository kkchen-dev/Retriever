import { Component } from '@angular/core';
import { NewsApiService } from './news-api.service';
import { feeds } from './mock_feeds';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Retriever'
  mArticles:Array<any>;
  mSources:Array<any>;
  feeds = feeds;

  constructor(private newsapi:NewsApiService){
    console.log('app component constructor called');
  }

  ngOnInit() {
        //load articles
      this.newsapi.initArticles().subscribe(data => this.mArticles = data['articles']);
    //load news sources
    this.newsapi.initSources().subscribe(data=> this.mSources = data['sources']);
    }

  searchArticles(source){
    console.log("selected source is: "+source);
    this.newsapi.getArticlesByID(source).subscribe(data => this.mArticles = data['articles']);
  }

}
