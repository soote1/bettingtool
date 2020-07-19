import { Injectable, NgZone } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SseService {
  constructor(private zone: NgZone) { }

  private getEventSource(url: string): EventSource {
    return new EventSource(url);
  }

  public connect(url: string, eventType: string): Observable<Event> {
    return new Observable(observer => {
      const eventSource = this.getEventSource(url);
      eventSource.addEventListener(eventType, (event: Event) => {
        this.zone.run(() => observer.next(event));
      });
    });
  }
}
