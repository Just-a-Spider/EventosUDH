export class User {
  id?: number;
  first_name?: string;
  last_name?: string;
  username?: string;
  email?: string;
  role?: string;
  code?: string;
  bio?: string;
  phone?: string;
  profile_picture?: string;
  linkedin?: string;

  constructor() {
    this.id = 0;
    this.first_name = '';
    this.last_name = '';
    this.username = '';
    this.email = '';
    this.role = '';
    this.code = '';
    this.bio = '';
    this.phone = '';
    this.profile_picture = 'https://via.placeholder.com/400';
    this.linkedin = '';
  }
}
