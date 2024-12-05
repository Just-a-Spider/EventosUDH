import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditEventForm } from './edit.component';

describe('EditComponent', () => {
  let component: EditEventForm;
  let fixture: ComponentFixture<EditEventForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [EditEventForm],
    }).compileComponents();

    fixture = TestBed.createComponent(EditEventForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
