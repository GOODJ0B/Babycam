import {Component, HostListener, OnInit} from '@angular/core';
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
  public width: number;
  public height: number;
  private videoResolutionWidth = 960;
  private videoResolutionHeight = 1080;

  constructor(public readonly babycamService: BabycamService) {
  }

  public ngOnInit(): void {
    this.updateValues();
    // setInterval(this.updateValues.bind(this), 60000);
    this.onResize(null);
  }

  @HostListener('window:resize', ['$event'])
  public onResize(event): void {
    let height = window.innerHeight;
    let width = window.innerWidth;

    const videoRatio = this.videoResolutionHeight / this.videoResolutionWidth;

    if (this.temperature !== undefined) {
      height -= 38;
    }
    if ((height / width) > (videoRatio)) {
      height = (width * videoRatio);
    } else {
      width = height / videoRatio;
    }

    this.width = width;
    this.height = height;
  }

  public updateValues(): void {
    this.babycamService.getValues().subscribe(values => {
      const previousTemp = this.temperature;
      this.temperature = values.temperature;
      this.pressure = values.pressure;
      this.humidity = values.humidity;
      if (previousTemp === undefined) {
        this.onResize(null);
      }
    });
  }

  public saveStill(): void {
    this.babycamService.saveStill().subscribe(() => {
      this.saveSuccessFul = true;
      // wait
      this.saveSuccessFul = false;
    });
  }
}
