import { Component, Input, OnInit, OnDestroy } from '@angular/core';

@Component({
  selector: 'event-clock',
  templateUrl: './live-clock.component.html',
  styleUrl: './live-clock.component.scss',
})
export class LiveClockComponent implements OnInit, OnDestroy {
  @Input() targetDate: Date = new Date();
  @Input() maxDate: Date = new Date();

  timeRemaining: string = '';
  severity: any = 'info';
  private intervalId: any;

  ngOnInit() {
    this.updateTimeRemaining();
    this.intervalId = setInterval(() => {
      this.updateTimeRemaining();
    }, 1000);
  }

  ngOnDestroy() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  }

  private updateTimeRemaining() {
    const now = new Date().getTime();
    const target = new Date(this.targetDate).getTime();
    const difference = target - now;

    if (difference <= 0) {
      const maxDifference = new Date(this.maxDate).getTime() - target;
      if (maxDifference > 0) {
        this.timeRemaining = 'Evento en curso';
        this.severity = 'success';
      } else {
        this.timeRemaining = 'Evento Finalizado';
        this.severity = 'danger';
      }
      if (this.intervalId) {
        clearInterval(this.intervalId);
      }
      return;
    }

    const days = Math.floor(difference / (1000 * 60 * 60 * 24));
    const hours = Math.floor(
      (difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((difference % (1000 * 60)) / 1000);

    this.timeRemaining = `${days}d ${hours}h ${minutes}m ${seconds}s`;
  }
}
