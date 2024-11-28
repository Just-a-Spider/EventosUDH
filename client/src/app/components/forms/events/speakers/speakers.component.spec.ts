import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpeakersForm } from './speakers.component';

describe('SpeakersComponent', () => {
  let component: SpeakersForm;
  let fixture: ComponentFixture<SpeakersForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SpeakersForm],
    }).compileComponents();

    fixture = TestBed.createComponent(SpeakersForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
