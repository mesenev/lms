export default interface UserModel {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  staff_for: Array<number>;
  avatar_url: string;
  thumbnail: string;
  email: string;
}

export interface AuthorModel extends UserModel {
  middle_name?: string;
}
