export default interface UserModel {
  id: number;
  username: string;
  firstName: string;
  lastName: string;
  staff_for: Array<boolean>;
}
