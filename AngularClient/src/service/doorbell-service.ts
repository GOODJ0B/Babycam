import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Values} from '../model/values';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DoorbellService {

  private url: string;
  public doorbellStatus: boolean;

  constructor(private readonly  httpClient: HttpClient) {
    this.url = 'http://192.168.0.31:5000';
  }

  public checkDoorbellStatus(): void {
    this.httpClient.get<boolean>(this.url + '/check')
      .subscribe(status => this.doorbellStatus = status);
  }

  public doorbellOn(): void {
    this.httpClient.get<boolean>(this.url + '/on')
      .subscribe(status => this.doorbellStatus = status);
  }

  public doorbellOff(): void {
    this.httpClient.get<boolean>(this.url + '/off')
      .subscribe(status => this.doorbellStatus = status);
  }
}
