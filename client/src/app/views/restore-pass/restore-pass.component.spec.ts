import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RestorePassView } from './restore-pass.component';

describe('RestorePassComponent', () => {
  let component: RestorePassView;
  let fixture: ComponentFixture<RestorePassView>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RestorePassView]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RestorePassView);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
