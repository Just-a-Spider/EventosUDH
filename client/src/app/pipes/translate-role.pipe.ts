import { Pipe, PipeTransform } from '@angular/core';

interface Translation {
  [key: string]: string;
}

@Pipe({
  name: 'translateRole',
})
export class TranslateRolePipe implements PipeTransform {
  private translations: Translation[] = [
    { student: 'Estudiante' },
    { coordinator: 'Coordinador' },
    { speaker: 'Ponente' },
  ];

  transform(value: string): string {
    if (!value) return value;
    const translation = this.translations.find(
      (translation) => translation[value]
    );
    return translation ? translation[value] : value;
  }
}
