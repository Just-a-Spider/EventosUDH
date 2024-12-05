import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpeakerDetailComponent } from './detail.component';

describe('DetailComponent', () => {
  let component: SpeakerDetailComponent;
  let fixture: ComponentFixture<SpeakerDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SpeakerDetailComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(SpeakerDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
