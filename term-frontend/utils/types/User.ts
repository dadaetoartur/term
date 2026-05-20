import type { IGroup } from './Group';

export interface IUser {
  [key: string]: string | boolean | Omit<IGroup, 'users'>[];
  id: string
  email: string
  is_active: boolean
  is_superuser: boolean
  is_verified: boolean
  first_name: string
  last_name: string
  middle_name: string
  mobile_phone: string
  role: string
  groups: Omit<IGroup, 'users'>[]
}
