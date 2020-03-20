import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-feed',
  templateUrl: './feed.component.html',
  styleUrls: ['./feed.component.css']
})
export class FeedComponent implements OnInit {
  private _feed;

  constructor() { }

  ngOnInit(): void {
  }
  @Input()
  set feed(feed) {
    this._feed = feed;
  }
  get feed() { return this._feed; }
}
