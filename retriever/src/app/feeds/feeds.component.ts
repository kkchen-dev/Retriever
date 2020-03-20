import { Component, OnInit } from '@angular/core';
import { feeds } from '../mock_feeds';

@Component({
  selector: 'app-feeds',
  templateUrl: './feeds.component.html',
  styleUrls: ['./feeds.component.css']
})
export class FeedsComponent implements OnInit {
  feeds = feeds;
  constructor() { }

  ngOnInit(): void {
  }

}
