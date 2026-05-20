import type { IUser } from '../types/User';

export const USER_ROLES = [
  {
    role: 'engineer',
    name: 'Инженер',
  }, {
    role: 'chief_engineer',
    name: 'Главный инженер',
  },
];

export const EMPTY_USER: IUser = {
  id: '',
  email: '',
  is_active: false,
  is_superuser: false,
  is_verified: false,
  first_name: '',
  last_name: '',
  middle_name: '',
  mobile_phone: '',
  role: '',
  groups: [],
};
