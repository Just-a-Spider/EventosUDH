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
    severity: '',
    label: 'Estudiante',
  },
  {
    mode: 'coordinator',
    icon: 'pi pi-users',
    severity: '',
    label: 'Coordinador',
  },
  {
    mode: 'speaker',
    icon: 'pi pi-bullhorn',
    severity: '',
    label: 'Ponente',
  },
];
