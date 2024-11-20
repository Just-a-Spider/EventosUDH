export interface ButtonInterface {
  mode: string;
  icon: string;
  severity: any;
  label: string;
}

export const BUTTONS: ButtonInterface[] = [
  {
    mode: 'student',
    icon: 'pi pi-book',
    severity: 'info',
    label: 'Estudiante',
  },
  {
    mode: 'coordinator',
    icon: 'pi pi-users',
    severity: 'warning',
    label: 'Coordinador',
  },
  {
    mode: 'speaker',
    icon: 'pi pi-bullhorn',
    severity: 'help',
    label: 'Ponente',
  },
];
