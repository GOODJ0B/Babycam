import {Component, OnInit} from '@angular/core';
import {Values} from '../model/values';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  public readonly title = 'BabyCam';
  public temperature: number;
  public humidity: number;
  public pressure: number;
  public apiUrl = 'http://192.168.0.33';

  public ngOnInit(): void {
    setInterval(this.updateValues.bind(this), 60000);
    const values = {
      temperature: 20.3,
      humidity: 33,
      pressure: 43,
    } as Values;
    console.log(JSON.stringify(values));
  }


  public updateValues(): void {

  }
}
