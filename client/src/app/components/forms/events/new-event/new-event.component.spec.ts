import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewEventForm } from './new-event.component';

describe('NewEventComponent', () => {
  let component: NewEventForm;
  let fixture: ComponentFixture<NewEventForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [NewEventForm],
    }).compileComponents();

    fixture = TestBed.createComponent(NewEventForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
