import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Values} from '../model/values';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class BabycamService {

  public url: string;
  private streamPort = 5001;
  private utilitiesPort = 5000;
  public streamUrl: string;
  public streamBaseUrl: string;

  constructor(private readonly  httpClient: HttpClient) {
    let url = window.location.href;
    // remove '/' from end
    url = url.substr(0, url.length - 1);

    // remove port number if exists
    for (let i = 'http://'.length; i < url.length; i++) {
      if (url[i] === ':') {
        url = url.substr(0, i);
      }
    }

    // url = 'http://192.168.0.32';
    this.url = url + ':' + this.utilitiesPort;
    this.streamUrl = url + ':' + this.streamPort + '/video';
    this.streamBaseUrl = url + ':' + this.streamPort;
  }

  public getValues(): Observable<Values> {
    return this.httpClient.get<Values>(this.url + '/values');
  }

  public saveStill(): Observable<null> {
    return this.httpClient.get<null>(this.streamBaseUrl + '/saveStill');
  }
}
