import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpeakersListComponent } from './list.component';

describe('ListComponent', () => {
  let component: SpeakersListComponent;
  let fixture: ComponentFixture<SpeakersListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SpeakersListComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(SpeakersListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
