import { Injectable } from '@angular/core';
import { SseService } from '../../../../core/sse/sse.service';
import { Observable } from 'rxjs';

@Injectable()
export class ArbsStreamService {
  url = 'http://localhost:3000/arbs';
  event = 'arb-found';

  constructor(private sseService: SseService) { }

  public onArbFound(): Observable<Event> {
    return this.sseService.connect(this.url, this.event);
  }
}
