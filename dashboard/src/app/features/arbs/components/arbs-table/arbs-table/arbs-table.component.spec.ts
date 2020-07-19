import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ArbsTableComponent } from './arbs-table.component';

describe('ArbsTableComponent', () => {
  let component: ArbsTableComponent;
  let fixture: ComponentFixture<ArbsTableComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ArbsTableComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ArbsTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
