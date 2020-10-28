import {Component, OnInit} from '@angular/core';
import {BabycamService} from '../service/babycam-service';

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

  constructor(public readonly babycamService: BabycamService) {
  }

  public ngOnInit(): void {
    this.updateValues();
    setInterval(this.updateValues.bind(this), 60000);
  }


  public updateValues(): void {
    this.babycamService.getValues().subscribe(values => {
      this.temperature = values.temperature;
      this.pressure = values.pressure;
      this.humidity = values.humidity;
    })
  }
}
