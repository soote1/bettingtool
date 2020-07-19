import { TestBed } from '@angular/core/testing';

import { ArbsStreamService } from './arbs-stream.service';

describe('ArbsStreamService', () => {
  let service: ArbsStreamService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ArbsStreamService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
