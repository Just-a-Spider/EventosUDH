import { Component, OnInit } from '@angular/core';
import { MessageService } from 'primeng/api';
import {
  FullNotification,
  PopUpNotification,
} from '../../../../classes/notifications.class';
import { NotificationsService } from '../../../../services/notifications.service';
import { ThemeService } from '../../../../services/misc/theme.service';

@Component({
  selector: 'header-notis',
  templateUrl: './notifications.component.html',
  styleUrl: './notifications.component.scss',
  providers: [MessageService],
})
export class NotificationsComponent implements OnInit {
  notifications: FullNotification[] = [];

  seenMode = false;

  constructor(
    public themesService: ThemeService,
    private notiService: NotificationsService,
    private messageService: MessageService
  ) {}

  ngOnInit() {
    // this.getNotifications();
    this.notiService.getNotificationUpdates().subscribe({
      next: (noti: PopUpNotification) => {
        this.showToast(noti);
        // this.getNotifications(this.seenMode);
      },
      error: (error: any) => {
        console.error(error);
      },
    });
  }
  ngOnDestroy() {
    this.notiService.close();
  }

  getNotifications(seen: boolean = false) {
    this.notiService.getNotifications(seen).subscribe({
      next: (notifications) => {
        this.notifications = notifications;
      },
      error: (error: any) => {
        console.error(error);
      },
    });
  }

  showToast(noti: PopUpNotification) {
    console.log('Showing toast:', noti);
    this.messageService.add({
      severity: 'warn',
      summary: 'Notificaciones',
      detail: noti.data,
    });
  }

  markSeen(notificationId: string) {
    this.notiService.markSeen(notificationId).subscribe({
      next: () => {
        this.getNotifications(this.seenMode);
      },
      error: (error: any) => {
        console.error(error);
      },
    });
  }

  getSeenUnseen() {
    this.seenMode = !this.seenMode;
    this.getNotifications(this.seenMode);
  }

  goToLicense(licenseId: string) {
    this.notiService.goToLicense(licenseId);
  }

  clearSeen() {
    this.notiService.clearSeen().subscribe({
      next: () => {
        this.getNotifications(this.seenMode);
        this.messageService.add({
          severity: 'success',
          summary: 'Notificaciones',
          detail: 'Notificaciones eliminadas',
        });
      },
      error: (error: any) => {
        console.error(error);
      },
    });
  }
}
