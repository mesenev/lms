export default interface UserModel {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  staff_for: Array<boolean>;
}
