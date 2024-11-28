import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResetPasswordView } from './reset-password.component';

describe('ResetPasswordComponent', () => {
  let component: ResetPasswordView;
  let fixture: ComponentFixture<ResetPasswordView>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ResetPasswordView],
    }).compileComponents();

    fixture = TestBed.createComponent(ResetPasswordView);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
