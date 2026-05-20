import type { IUser } from './User';

export interface IGroup {
  [key: string]: string | Omit<IUser, 'groups'>[]
  id: string
  name: string
  description: string
  users: Omit<IUser, 'groups'>[]
}
