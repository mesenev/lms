export default interface UserModel {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  study_group: string;
  staff_for: Array<number>;
  avatar_url: string;
  thumbnail: string;
  email: string;
  cats_account: number|null;
  current_control_work: number|null;
}

export interface AuthorModel extends UserModel {
  middle_name?: string;
}
