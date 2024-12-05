import { Component } from '@angular/core';
import { User } from '../../classes/user.class';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { FileUpload } from 'primeng/fileupload';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.scss',
  providers: [MessageService],
})
export class ProfileView {
  newPassword: string = '';
  confirmPassword: string = '';
  user: User = new User();
  mobile = false;
  mainClass =
    'flex flex-row gap-8 w-screen justify-content-center align-items-start p-4 mt-8';
  mainCardClass = 'profile-card';
  uploadedImage: File | null = null;

  constructor(
    private authService: AuthService,
    private router: Router,
    private messagesService: MessageService
  ) {}

  ngOnInit() {
    this.user = this.authService.getUserValue();
  }

  goBack() {
    // Redirect to the previous page
    this.router.navigate(['/']);
  }

  changePassword() {
    this.messagesService.add({
      severity: 'info',
      summary: 'No implementado',
      detail: 'Esta función no ha sido implementada aún.',
    });
  }

  uploadPfp(event: any, fileUpload: FileUpload) {
    this.uploadedImage = event.files[0];
    fileUpload.clear();
    const reader = new FileReader();
    if (this.uploadedImage) {
      reader.readAsDataURL(this.uploadedImage);
    }
    reader.onload = () => {
      this.user.profile_picture = reader.result as string;
    };
  }

  saveProfile() {
    this.authService.saveProfile(this.uploadedImage, this.user).subscribe({
      next: () => {
        this.messagesService.add({
          severity: 'success',
          summary: 'Imagen de perfil actualizada',
          detail: 'La imagen de perfil se ha actualizado correctamente.',
        });
      },
      error: (error) => {
        this.messagesService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'No se pudo actualizar la imagen de perfil.',
        });
      },
    });
  }
}
