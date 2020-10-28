import {HttpClient} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Values} from '../model/values';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class BabycamService {

  public url: string;
  private port = 5000;
  public streamUrl: string;

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

    // add port number of backend
    this.url = url + ':' + this.port;
    this.streamUrl = this.url + '/stream.mjpg';
  }

  public getValues(): Observable<Values> {
    return this.httpClient.get<Values>(this.url + '/values');
  }
}
