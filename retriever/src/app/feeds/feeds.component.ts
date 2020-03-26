import { Component, OnInit } from '@angular/core';
import { news_feeds } from '../../../../python_modules/news_feeds';

@Component({
  selector: 'app-feeds',
  templateUrl: './feeds.component.html',
  styleUrls: ['./feeds.component.css']
})
export class FeedsComponent implements OnInit {
  feeds = news_feeds;
  constructor() { }

  ngOnInit(): void {
  }

}
