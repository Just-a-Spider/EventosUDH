import { NgModule } from '@angular/core';

// PrimeNG stuff
import { AccordionModule } from 'primeng/accordion';
import { AvatarModule } from 'primeng/avatar';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';
import { ChipModule } from 'primeng/chip';
import { DialogModule } from 'primeng/dialog';
import { DividerModule } from 'primeng/divider';
import { InputSwitchModule } from 'primeng/inputswitch';
import { InputTextModule } from 'primeng/inputtext';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { KeyFilterModule } from 'primeng/keyfilter';
import { MessagesModule } from 'primeng/messages';
import { PanelModule } from 'primeng/panel';
import { PasswordModule } from 'primeng/password';
import { RadioButtonModule } from 'primeng/radiobutton';
import { TableModule } from 'primeng/table';
import { TabViewModule } from 'primeng/tabview';
import { ToastModule } from 'primeng/toast';

@NgModule({
  exports: [
    AccordionModule,
    AvatarModule,
    ButtonModule,
    RadioButtonModule,
    CardModule,
    ChipModule,
    DialogModule,
    DividerModule,
    InputTextModule,
    InputTextareaModule,
    InputSwitchModule,
    KeyFilterModule,
    MessagesModule,
    PanelModule,
    PasswordModule,
    TableModule,
    TabViewModule,
    ToastModule,
  ],
})
export class PrimeNGModule {}
