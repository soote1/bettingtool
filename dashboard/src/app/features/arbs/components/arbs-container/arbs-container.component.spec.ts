import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ArbsContainerComponent } from './arbs-container.component';

describe('ArbsContainerComponent', () => {
  let component: ArbsContainerComponent;
  let fixture: ComponentFixture<ArbsContainerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ArbsContainerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ArbsContainerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
